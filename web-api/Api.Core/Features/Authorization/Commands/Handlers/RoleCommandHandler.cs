using Api.Core.Bases;
using Api.Core.Features.Authorization.Commands.Models;
using Api.Service.Abstracts;
using MediatR;

namespace Api.Core.Features.Authorization.Commands.Handlers
{
    public class RoleCommandHandler : ResponseHandler,
                                                IRequestHandler<AddRoleCommand, Response<string>>,
                                                IRequestHandler<DeleteRoleCommand, Response<string>>,
                                                IRequestHandler<EditRoleCommand, Response<string>>,
                                                IRequestHandler<UpdateUserRolesCommand, Response<string>>

    {
        #region Fields

        IAuthorizationService _authorizationService;
        #endregion
        #region Constructor
        public RoleCommandHandler(IAuthorizationService authorizationService)
        {

            _authorizationService = authorizationService;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<string>> Handle(AddRoleCommand request, CancellationToken cancellationToken)
        {
            var result = await _authorizationService.AddRoleAsync(request.RoleName);
            if (result == "Success")
            {
                return Success(result);
            }
            else
            {
                return BadRequest<string>(result);
            }
        }
        public async Task<Response<string>> Handle(EditRoleCommand request, CancellationToken cancellationToken)
        {
            var result = await _authorizationService.EditRoleAsync(request);
            if (result == "Success")
            {
                return Success(result);
            }
            else if (result == "NotFound")
            {
                return NotFound<string>(result);
            }
            else
            {
                return BadRequest<string>(result);
            }
        }
        public async Task<Response<string>> Handle(DeleteRoleCommand request, CancellationToken cancellationToken)
        {
            var result = await _authorizationService.DeleteRoleAsync(request.Id);
            if (result == "NotFound")
            {
                return NotFound<string>(result);
            }
            else if (result == "Used")
            {
                return BadRequest<string>(result);
            }
            else if (result == "Success")
            {
                return Success<string>(result);
            }
            else
            {
                return BadRequest<string>(result);
            }
        }
        public async Task<Response<string>> Handle(UpdateUserRolesCommand request, CancellationToken cancellationToken)
        {
            var result = await _authorizationService.UpdateUserRole(request);
            if (result == "UserNotFound") return NotFound<string>(result);
            else if (result == "Failed To RemoveOldRoles" || result == "Failed To AddNewRoles" || result == "Failed To UpdateUserRoles") return BadRequest<string>(result);
            else
            {
                return Success(result);
            }
        }
        #endregion
    }
}
