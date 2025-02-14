using Api.Core.Bases;
using Api.Core.Features.Authentication.Command.Models;
using Api.Data.Entities.Identity;
using Api.Data.Helpers;
using Api.Service.Abstracts;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace Api.Core.Features.Authentication.Command.Handlers
{
    public class AuthenticationCommandHandler : ResponseHandler,
                                                            IRequestHandler<SignInCommand, Response<JWTAuthRes>>,
                                                            IRequestHandler<RefreshTokenCommand, Response<JWTAuthRes>>,
                                                            IRequestHandler<ResetPasswordCommand, Response<string>>,
                                                            IRequestHandler<SendResetPasswordCommand, Response<string>>

    {
        #region Fields
        private readonly UserManager<Organization> _userManager;
        private readonly SignInManager<Organization> _signInManager;
        private readonly IAuthenticationService _authenticationService;
        #endregion
        #region Constructor
        public AuthenticationCommandHandler(UserManager<Organization> userManager,
                                             SignInManager<Organization> signInManager,
                                             IAuthenticationService authenticationService)
        {
            _userManager = userManager;
            _signInManager = signInManager;
            _authenticationService = authenticationService;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<JWTAuthRes>> Handle(SignInCommand request, CancellationToken cancellationToken)
        {
            var user = await _userManager.FindByNameAsync(request.UserName);
            if (user == null) { return NotFound<JWTAuthRes>("User Not Found"); }
            var signinresult = await _userManager.CheckPasswordAsync(user, request.Password);
            if (!user.EmailConfirmed) return BadRequest<JWTAuthRes>("Confirm your email");
            if (!signinresult)
            {
                return BadRequest<JWTAuthRes>("Username or Password is not correct");
            }
            var accesstoken = await _authenticationService.GetJWTToken(user);
            return Success(accesstoken);
        }
        public async Task<Response<JWTAuthRes>> Handle(RefreshTokenCommand request, CancellationToken cancellationToken)
        {
            var JWTToken = _authenticationService.ReadJWTToken(request.AccessToken);
            var validateresult = await _authenticationService.ValidateDetails(JWTToken, request.AccessToken, request.RefreshToken);
            switch (validateresult)
            {
                case ("AlgorithmIsWrong", null): return Unauthorized<JWTAuthRes>("AlgorithmIsWrong");
                case ("TokenIsNotExpired", null): return Unauthorized<JWTAuthRes>("TokenIsNotExpired");
                case ("RefreshTokenIsNotFound", null): return Unauthorized<JWTAuthRes>("RefreshTokenIsNotFound");
                case ("RefreshTokenIsExpired", null): return Unauthorized<JWTAuthRes>("RefreshTokenIsExpired");
            }

            var (userid, expiredate) = validateresult;
            var user = await _userManager.FindByIdAsync(userid);
            if (user == null)
            {
                return NotFound<JWTAuthRes>();
            }
            var result = await _authenticationService.GetRefreshToken(user, JWTToken, expiredate, request.RefreshToken);
            return Success(result);
        }
        public async Task<Response<string>> Handle(SendResetPasswordCommand request, CancellationToken cancellationToken)
        {
            var result = await _authenticationService.SendResetPasswordCode(request.Email);
            switch (result)
            {
                case "UserNotFound": return BadRequest<string>(result);
                case "ErrorInUpdateUser": return BadRequest<string>(result);
                case "Failed": return BadRequest<string>(result);
                case "Success": return Success("");
                default: return BadRequest<string>(result);
            }
        }
        public async Task<Response<string>> Handle(ResetPasswordCommand request, CancellationToken cancellationToken)
        {
            var result = await _authenticationService.ResetPassword(request.Email, request.Password);
            switch (result)
            {
                case "UserNotFound": return BadRequest<string>(result);
                case "Failed": return BadRequest<string>(result);
                case "Success": return Success("");
                default: return BadRequest<string>(result);
            }
        }

        #endregion
    }
}
