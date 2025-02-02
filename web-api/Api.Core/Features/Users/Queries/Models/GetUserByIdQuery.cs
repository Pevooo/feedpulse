using Api.Core.Bases;
using Api.Core.Features.Users.Queries.Response;
using MediatR;

namespace Api.Core.Features.Users.Queries.Models
{
    public class GetUserByIdQuery : IRequest<Response<GetUserByIdResponse>>
    {
        public string Id { get; set; }
    }
}
