using Api.Core.Bases;
using Api.Data.Helpers;
using MediatR;

namespace Api.Core.Features.Authentication.Command.Models
{
    public class SignInCommand : IRequest<Response<JWTAuthRes>>
    {
        public string UserName { get; set; }
        public string Password { get; set; }
    }
}
