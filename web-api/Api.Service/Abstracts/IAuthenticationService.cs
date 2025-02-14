using Api.Data.Entities.Identity;
using Api.Data.Helpers;
using System.IdentityModel.Tokens.Jwt;

namespace Api.Service.Abstracts
{
    public interface IAuthenticationService
    {
        public Task<JWTAuthRes> GetJWTToken(Organization organization);
        public Task<JWTAuthRes> GetRefreshToken(Organization organization, JwtSecurityToken jwtToken, DateTime? expiryDate, string refreshToken);
        public Task<(string, DateTime?)> ValidateDetails(JwtSecurityToken JwtToken, string accessToken, string RefreshToken);
        public JwtSecurityToken ReadJWTToken(string token);
        public Task<string> ValidateToken(string accessToken);
        public Task<string> ConfirmEmail(string userid, string code);
        public Task<string> SendResetPasswordCode(string Email);
        public Task<string> ConfirmResetPassword(string Code, string Email);
        public Task<string> ResetPassword(string Email, string password);
    }
}
