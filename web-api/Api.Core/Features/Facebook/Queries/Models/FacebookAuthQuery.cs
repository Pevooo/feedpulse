using Api.Core.Bases;
using MediatR;

namespace Api.Core.Features.Facebook.Queries.Models
{
    public class FacebookAuthQuery : IRequest<Response<string>>
    {
        public string token { get; set; }
        public string UserAppId { get; set; }
    }
}
