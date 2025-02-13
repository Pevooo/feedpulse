using Api.Core.Bases;
using Api.Core.Features.Authentication.Queries.Models;
using Api.Service.Abstracts;
using MediatR;

namespace Api.Core.Features.Authentication.Queries.Handlers
{
    public class AuthenticationQueriesHandlers : ResponseHandler,
                                                IRequestHandler<AuthorizeUserQuery, Response<string>>,
                                                IRequestHandler<ConfirmEmailQuery, Response<string>>,
                                                IRequestHandler<ConfirmResetPasswordQuery, Response<string>>
    {
        #region Fields
        private readonly IAuthenticationService _authenticationService;
        #endregion
        #region Constructors
        public AuthenticationQueriesHandlers(IAuthenticationService authenticationService)
        {
            _authenticationService = authenticationService;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<string>> Handle(AuthorizeUserQuery request, CancellationToken cancellationToken)
        {
            var result = await _authenticationService.ValidateToken(request.AccessToken);
            if (result == "NotExpired")
                return Success(result);
            return Unauthorized<string>(result);
        }
        public async Task<Response<string>> Handle(ConfirmEmailQuery request, CancellationToken cancellationToken)
        {
            var result = await _authenticationService.ConfirmEmail(request.UserId, request.Code);
            if (result == "ErrorWhenConfirmEmail" || result == "Useridisnotvalid" || result == "ErrorWhenConfirmEmail")
            {
                return BadRequest<string>(result);
            }
            return Success(result);
        }
        public async Task<Response<string>> Handle(ConfirmResetPasswordQuery request, CancellationToken cancellationToken)
        {
            var result = await _authenticationService.ConfirmResetPassword(request.Code, request.Email);
            if (result == "UserNotFound")
            {
                return NotFound<string>(result);
            }
            else if (result == "Failed")
            {
                return BadRequest<string>(result);
            }
            else
            {
                return Success(result);
            }
        }
        #endregion
    }
}
