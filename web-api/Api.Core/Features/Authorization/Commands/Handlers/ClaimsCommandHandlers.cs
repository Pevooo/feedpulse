using Api.Core.Bases;
using Api.Core.Features.Authorization.Commands.Models;
using Api.Service.Abstracts;
using MediatR;

namespace Api.Core.Features.Authorization.Commands.Handlers
{
    public class ClaimsCommandHandlers : ResponseHandler, IRequestHandler<UpdateUserClaimsCommand, Response<string>>
    {
        #region Fileds
        private readonly IAuthorizationService _authorizationService;

        #endregion
        #region Constructors
        public ClaimsCommandHandlers(IAuthorizationService authorizationService)
        {
            _authorizationService = authorizationService;
        }

        #endregion
        #region Functions
        public async Task<Response<string>> Handle(UpdateUserClaimsCommand request, CancellationToken cancellationToken)
        {
            var result = await _authorizationService.UpdateUserClaims(request);
            switch (result)
            {
                case "UserIsNull": return NotFound<string>(result);
                case "FailedToRemoveOldClaims": return BadRequest<string>(result);
                case "FailedToAddNewClaims": return BadRequest<string>(result);
                case "FailedToUpdateClaims": return BadRequest<string>(result);
            }
            return Success<string>(result);
        }
        #endregion
    }
}
