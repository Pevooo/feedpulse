using Api.Core.Bases;
using Api.Core.Features.Authorization.Queries.Response;
using Api.Core.Features.Facebook.Queries.Models;
using Api.Core.Features.Facebook.Queries.Responses;
using Api.Data.DTOS;
using Api.Data.Entities.Identity;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;
using Microsoft.AspNetCore.Identity;

namespace Api.Core.Features.Facebook.Queries.Handler
{
    public class FacebookQueriesHandler : ResponseHandler, IRequestHandler<FacebookAuthQuery, Response<string>>,
        IRequestHandler<GetFacebookPageListQuery,Response<List<SingleFacebookPageResponse>>>

	{
        #region Fields
        IFacebookService _facebookService;
		private readonly IMapper _mapper;
		UserManager<AppUser> _userManager;
        #endregion
        #region Constructor
        public FacebookQueriesHandler(IFacebookService facebookService, UserManager<AppUser> userManager, IMapper mapper)
        {
            _facebookService = facebookService;
            _userManager = userManager;
            _mapper = mapper;
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

        public async Task<Response<List<SingleFacebookPageResponse>>> Handle(GetFacebookPageListQuery request, CancellationToken cancellationToken)
        {
            var pages = await _facebookService.GetFacebookPages(request.AccessToken);

            var result = pages.Select(page => new SingleFacebookPageResponse
			{
				Id = page.Id,
				Name = page.Name,
				AccessToken = page.AccessToken
			}).ToList();

			return Success(result);
		}


		#endregion
	}
}
