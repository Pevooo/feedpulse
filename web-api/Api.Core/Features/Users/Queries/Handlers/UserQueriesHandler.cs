using Api.Core.Bases;
using Api.Core.Features.Users.Queries.Models;
using Api.Core.Features.Users.Queries.Response;
using Api.Data.Entities.Identity;
using AutoMapper;
using MediatR;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using School.Core.Wrappers;

namespace Api.Core.Features.Users.Queries.Handlers
{
    public class UserQueriesHandler : ResponseHandler,
                                IRequestHandler<GetUserByIdQuery, Response<GetUserByIdResponse>>,
                                IRequestHandler<GetPaginatedListQuery, PaginatedResult<GetUserListResponse>>
    {
        #region fields
        private readonly IMapper _mapper;
        private readonly UserManager<AppUser> _userManager;
        #endregion
        #region constructor
        public UserQueriesHandler(IMapper mapper, UserManager<AppUser> userManager)
        {
            _mapper = mapper;
            _userManager = userManager;
        }
        #endregion
        #region HandleFunctions

        public async Task<Response<GetUserByIdResponse>> Handle(GetUserByIdQuery request, CancellationToken cancellationToken)
        {
            var user = await _userManager.Users.SingleOrDefaultAsync(x => x.Id == request.Id);
            if (user == null)
            {
                return NotFound<GetUserByIdResponse>("User is not Exist");
            }
            var result = _mapper.Map<GetUserByIdResponse>(user);
            return Success<GetUserByIdResponse>(result);
        }

        public async Task<PaginatedResult<GetUserListResponse>> Handle(GetPaginatedListQuery request, CancellationToken cancellationToken)
        {
            var users = _userManager.Users.AsQueryable();
            var paginatedList = await _mapper.ProjectTo<GetUserListResponse>(users).ToPaginatedListAsync(request.PageNumber, request.PageSize);
            return paginatedList;
        }

        #endregion
    }
}
