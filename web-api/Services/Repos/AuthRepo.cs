using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using web_api.Dtos.Authentication;
using web_api.Dtos.Results;
using web_api.Helpers;
using web_api.Models;
using web_api.Services.Interfaces;
using Microsoft.EntityFrameworkCore;


namespace web_api.Services.Repos
{
    public class AuthRepo : IAuth
    {
        private readonly UserManager<Organization> _organizationManager;
        private readonly RoleManager<IdentityRole> _roleManager;
        private readonly JWT _jwt;
        public AuthRepo(UserManager<Organization> organizationManager, RoleManager<IdentityRole> roleManager, IOptions<JWT> jwt)
        {
            _organizationManager = organizationManager;
            _roleManager = roleManager;
            _jwt = jwt.Value;

        }

        public async Task<AuthResult> RegisterAsync(RegisterDto model)
        {
            if (await _organizationManager.FindByEmailAsync(model.Email) != null)
            {
                return new AuthResult { Message = "Email is Not Valid" };
            }
            if (await _organizationManager.FindByNameAsync(model.UserName) != null)
            {
                return new AuthResult { Message = "Username Is exist before" };
            }
            var Organization = new Organization
            {
                UserName = model.UserName,
                Email = model.Email,
                PhoneNumber = model.PhoneNumber,
                City = model.City,
                Country = model.Country,
                Description = model.Description,
                OrganizationName = model.OrganizationName
            };
            var result = await _organizationManager.CreateAsync(Organization, model.Password);
            if (!result.Succeeded)
            {
                var errors = string.Empty;

                foreach (var error in result.Errors)
                    errors += $"{error.Description},";

                return new AuthResult { Message = errors };
            }
            await _organizationManager.AddToRoleAsync(Organization, "Organization");
            var jwtSecurityToken = await CreateJwtToken(Organization);
            return new AuthResult
            {
                Email = Organization.Email,
                ExpiresOn = jwtSecurityToken.ValidTo,
                IsAuthenticated = true,
                Roles = new List<string> { "Orgnaization" },
                Token = new JwtSecurityTokenHandler().WriteToken(jwtSecurityToken),
                Username = Organization.UserName,

            };
        }

        public async Task<bool> RevokeTokenAsync(string token)
        {
            var user = await _organizationManager.Users.SingleOrDefaultAsync(u => u.RefreshTokens.Any(t => t.Token == token));

            if (user == null)
                return false;

            var refreshToken = user.RefreshTokens.Single(t => t.Token == token);

            if (!refreshToken.IsActive)
                return false;

            refreshToken.RevokedOn = DateTime.UtcNow;

            await _organizationManager.UpdateAsync(user);

            return true;
        }
        public async Task<AuthResult> RefreshTokenAsync(string token)
        {
            var AuthResult = new AuthResult();

            var user = await _organizationManager.Users.SingleOrDefaultAsync(u => u.RefreshTokens.Any(t => t.Token == token));

            if (user == null)
            {
                AuthResult.Message = "Invalid token";
                return AuthResult;
            }

            var refreshToken = user.RefreshTokens.Single(t => t.Token == token);

            if (!refreshToken.IsActive)
            {
                AuthResult.Message = "Inactive token";
                return AuthResult;
            }

            refreshToken.RevokedOn = DateTime.UtcNow;

            var newRefreshToken = GenerateRefreshToken();
            user.RefreshTokens.Add(newRefreshToken);
            await _organizationManager.UpdateAsync(user);

            var jwtToken = await CreateJwtToken(user);
            AuthResult.IsAuthenticated = true;
            AuthResult.Token = new JwtSecurityTokenHandler().WriteToken(jwtToken);
            AuthResult.Email = user.Email;
            AuthResult.Username = user.UserName;
            var roles = await _organizationManager.GetRolesAsync(user);
            AuthResult.Roles = roles.ToList();
            AuthResult.RefreshToken = newRefreshToken.Token;
            AuthResult.RefreshTokenExpiration = newRefreshToken.ExpiresOn;

            return AuthResult;
        }

        private async Task<JwtSecurityToken> CreateJwtToken(Organization org)
        {
            var userClaims = await _organizationManager.GetClaimsAsync(org);
            var roles = await _organizationManager.GetRolesAsync(org);
            var roleClaims = new List<Claim>();

            foreach (var role in roles)
                roleClaims.Add(new Claim("roles", role));

            var claims = new[]
            {
                new Claim(JwtRegisteredClaimNames.Sub, org.UserName),
                new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
                new Claim(JwtRegisteredClaimNames.Email, org.Email),
                new Claim("uid", org.Id)
            }
            .Union(userClaims)
            .Union(roleClaims);

            var symmetricSecurityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_jwt.Key));
            var signingCredentials = new SigningCredentials(symmetricSecurityKey, SecurityAlgorithms.HmacSha256);

            var jwtSecurityToken = new JwtSecurityToken(
                issuer: _jwt.Issuer,
                audience: _jwt.Audience,
                claims: claims,
                expires: DateTime.UtcNow.AddMinutes(_jwt.DurationInMinutes),
                signingCredentials: signingCredentials);

            return jwtSecurityToken;
        }
        private RefreshToken GenerateRefreshToken()
        {
            var randomNumber = new byte[32];

            using var generator = new RNGCryptoServiceProvider();

            generator.GetBytes(randomNumber);

            return new RefreshToken
            {
                Token = Convert.ToBase64String(randomNumber),
                ExpiresOn = DateTime.UtcNow.AddDays(7),
                CreatedOn = DateTime.UtcNow
            };
        }
        public async Task<AuthResult> LoginAsync(LoginDto model)
        {
            var AuthResult = new AuthResult();

            var user = await _organizationManager.FindByEmailAsync(model.Email);

            if (user is null || !await _organizationManager.CheckPasswordAsync(user, model.Password))
            {
                AuthResult.Message = "Email or Password is incorrect!";
                return AuthResult;
            }

            var jwtSecurityToken = await CreateJwtToken(user);
            var rolesList = await _organizationManager.GetRolesAsync(user);

            AuthResult.IsAuthenticated = true;
            AuthResult.Token = new JwtSecurityTokenHandler().WriteToken(jwtSecurityToken);
            AuthResult.Email = user.Email;
            AuthResult.Username = user.UserName;
            AuthResult.ExpiresOn = jwtSecurityToken.ValidTo;
            AuthResult.Roles = rolesList.ToList();

            if (user.RefreshTokens.Any(t => t.IsActive))
            {
                var activeRefreshToken = user.RefreshTokens.FirstOrDefault(t => t.IsActive);
                AuthResult.RefreshToken = activeRefreshToken.Token;
                AuthResult.RefreshTokenExpiration = activeRefreshToken.ExpiresOn;
            }
            else
            {
                var refreshToken = GenerateRefreshToken();
                AuthResult.RefreshToken = refreshToken.Token;
                AuthResult.RefreshTokenExpiration = refreshToken.ExpiresOn;
                user.RefreshTokens.Add(refreshToken);
                await _organizationManager.UpdateAsync(user);
            }

            return AuthResult;
        }

    }
}
