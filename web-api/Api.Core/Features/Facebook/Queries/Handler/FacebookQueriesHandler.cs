using Api.Core.Bases;
using Api.Core.Features.Facebook.Queries.Models;
using Api.Data.Entities.Identity;
using Api.Service.Abstracts;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace Api.Core.Features.Facebook.Queries.Handler
{
    public class FacebookQueriesHandler : ResponseHandler, IRequestHandler<FacebookAuthQuery, Response<string>>
    {
        #region Fields
        IFacebookService _facebookService;
        UserManager<AppUser> _userManager;
        #endregion
        #region Constructor
        public FacebookQueriesHandler(IFacebookService facebookService, UserManager<AppUser> userManager)
        {
            _facebookService = facebookService;
            _userManager = userManager;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<string>> Handle(FacebookAuthQuery request, CancellationToken cancellationToken)
        {
            if (request.token == null)
            {
                return NotFound<string>("Token Is Empty");
            }
            var user = await _userManager.FindByIdAsync(request.UserAppId);
            if (user == null) { return NotFound<string>("Invalid UserId"); }
            if (!await _facebookService.ValidateFacebookToken(request.token))
            {
                return BadRequest<string>("Invalid Token");
            }
            var longlivedtoken = await _facebookService.GetLongLivedUserToken(request.token);
            user.FacebookAccessToken = longlivedtoken;
            _ = await _userManager.UpdateAsync(user);
            return Success<string>("Success");

        }
        #endregion
    }
}
