using Api.Core.Bases;
using MediatR;

namespace Api.Core.Features.Authentication.Command.Models
{
    public class SendResetPasswordCommand : IRequest<Response<string>>
    {
        public string Email { get; set; }
    }
}
