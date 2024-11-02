using web_api.Dtos.Authentication;
using web_api.Dtos.Results;

namespace web_api.Services.Interfaces
{
    public interface IAuth
    {
        Task<AuthResult> RegisterAsync(RegisterDto model);
        Task<AuthResult> RefreshToken(string token);
        Task<bool> RevokeTokenAsync(string token);
    }
}
