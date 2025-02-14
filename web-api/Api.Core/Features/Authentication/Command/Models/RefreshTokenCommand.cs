using Api.Core.Bases;
using Api.Data.Helpers;
using MediatR;

namespace Api.Core.Features.Authentication.Command.Models
{
    public class RefreshTokenCommand : IRequest<Response<JWTAuthRes>>
    {
        public string AccessToken { get; set; }
        public string RefreshToken { get; set; }
    }
}
