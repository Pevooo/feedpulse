using Api.Data.DTOS;

namespace Api.Service.Abstracts
{
    public interface IFacebookService
    {
        Task<bool> ValidateFacebookToken(string token);
        Task<string> GetLongLivedUserToken(string token);
		Task<List<FacebookPage>> GetFacebookPages(string accessToken);
	}
}
