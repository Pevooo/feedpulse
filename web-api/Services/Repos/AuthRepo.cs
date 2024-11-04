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
                Roles = new List<string> { "Organization" },
                Token = new JwtSecurityTokenHandler().WriteToken(jwtSecurityToken),
                Username = Organization.UserName,
            };
        }

        public Task<bool> RevokeTokenAsync(string token)
        {
            throw new NotImplementedException();
        }

        public Task<AuthResult> RefreshToken(string token)
        {
            throw new NotImplementedException();
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
                ExpiresOn = DateTime.UtcNow.AddDays(30),
                CreatedOn = DateTime.UtcNow
            };
        }
    }
}
