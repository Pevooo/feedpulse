using Api.Core.Features.Users.Queries.Response;
using MediatR;
using School.Core.Wrappers;

namespace Api.Core.Features.Users.Queries.Models
{
    public class GetPaginatedListQuery : IRequest<PaginatedResult<GetUserListResponse>>
    {
        public int PageNumber { get; set; }
        public int PageSize { get; set; }
    }
}
