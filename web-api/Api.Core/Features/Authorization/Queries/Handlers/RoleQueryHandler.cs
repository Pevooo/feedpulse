using Api.Core.Bases;
using Api.Core.Features.Authorization.Queries.Models;
using Api.Core.Features.Authorization.Queries.Response;
using Api.Data.DTOS;
using Api.Data.Entities.Identity;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace Api.Core.Features.Authorization.Queries.Handlers
{
    public class RoleQueryHandler : ResponseHandler, IRequestHandler<GetRoleByIdQuery, Response<GetRoleByIdResponse>>
                                                   , IRequestHandler<GetRoleListQuery, Response<List<GetRolesListResponse>>>
                                                   , IRequestHandler<ManageUserRolesQuery, Response<ManageUserRolesResponse>>

    {
        #region Fields
        private readonly IAuthorizationService _authorizationService;
        private readonly IMapper _mapper;
        private readonly UserManager<Organization> _userManager;
        #endregion
        #region Constructors
        public RoleQueryHandler(IAuthorizationService authorizationService,
                                IMapper mapper,
                                UserManager<Organization> userManager)
        {
            _authorizationService = authorizationService;
            _mapper = mapper;
            _userManager = userManager;
        }

        #endregion
        #region HandleFunctions
        public async Task<Response<List<GetRolesListResponse>>> Handle(GetRoleListQuery request, CancellationToken cancellationToken)
        {
            var roles = await _authorizationService.GetRolesList();
            var result = _mapper.Map<List<GetRolesListResponse>>(roles);
            return Success(result);
        }
        public async Task<Response<GetRoleByIdResponse>> Handle(GetRoleByIdQuery request, CancellationToken cancellationToken)
        {
            var role = await _authorizationService.GetRoleById(request.RoleId);
            if (role == null)
            {
                return NotFound<GetRoleByIdResponse>();
            }
            var result = _mapper.Map<IdentityRole, GetRoleByIdResponse>(role);
            return Success(result);
        }
        public async Task<Response<ManageUserRolesResponse>> Handle(ManageUserRolesQuery request, CancellationToken cancellationToken)
        {
            var user = await _userManager.FindByIdAsync(request.UserId);
            if (user == null)
            {
                return NotFound<ManageUserRolesResponse>("User Not Found");
            }
            var response = await _authorizationService.ManageUserRolesData(user);
            return Success(response);

        }
        #endregion
    }
}
