using Api.Data.DTOS;
using Api.Data.Helpers;
using Api.Infrastructure.Data;
using Api.Service.Abstracts;
using Microsoft.Extensions.Options;
using System.Text.Json;

namespace Api.Service.Implementation
{
    public class FacebookService : IFacebookService
    {
        #region Fields
        private readonly FacebookSettings _facebookSettings;
        private readonly HttpClient _httpClient;
        private readonly ApplicationDbContext _dbcontext;
        #endregion

        #region Constructor
        public FacebookService(IOptions<FacebookSettings> facebookSettings, HttpClient httpClient, ApplicationDbContext dbContext)
        {
            _facebookSettings = facebookSettings.Value;
            _httpClient = httpClient;
            _dbcontext = dbContext;
        }
        #endregion

        #region HandleFunctions

        public async Task<string> GetLongLivedUserToken(string token)
        {
            string url = $"https://graph.facebook.com/v18.0/oauth/access_token" +
                         $"?grant_type=fb_exchange_token" +
                         $"&client_id={_facebookSettings.AppId}" +
                         $"&client_secret={_facebookSettings.AppSecret}" +
                         $"&fb_exchange_token={token}";

            var response = await _httpClient.GetStringAsync(url);
            var json = JsonSerializer.Deserialize<JsonElement>(response);

            return json.GetProperty("access_token").GetString();
        }

        public async Task<bool> ValidateFacebookToken(string token)
        {
            string appAccessToken = $"{_facebookSettings.AppId}|{_facebookSettings.AppSecret}";

            string url = $"https://graph.facebook.com/debug_token?input_token={token}&access_token={appAccessToken}";

            var response = await _httpClient.GetStringAsync(url);
            var json = JsonSerializer.Deserialize<JsonElement>(response);

            return json.GetProperty("data").GetProperty("is_valid").GetBoolean();
        }

        public async Task<List<FacebookPage>> GetFacebookPages(string accessToken)
        {
            string url = $"https://graph.facebook.com/me/accounts?access_token={accessToken}";

            var response = await _httpClient.GetStringAsync(url);
            var pagesData = JsonSerializer.Deserialize<JsonElement>(response);

            var pages = pagesData.GetProperty("data").EnumerateArray().Select(p => new FacebookPage
            {
                Id = p.GetProperty("id").GetString(),
                Name = p.GetProperty("name").GetString(),
                AccessToken = p.TryGetProperty("access_token", out var token) ? token.GetString() : null
            }).ToList();

            return pages;
        }
        public async Task<List<FacebookPage>> GetUnregisteredFacebookPages(string accessToken)
        {
            string url = $"https://graph.facebook.com/me/accounts?access_token={accessToken}";

            var response = await _httpClient.GetStringAsync(url);
            var pagesData = JsonSerializer.Deserialize<JsonElement>(response);

            var pages = pagesData.GetProperty("data").EnumerateArray().Select(p => new FacebookPage
            {
                Id = p.GetProperty("id").GetString(),
                Name = p.GetProperty("name").GetString(),
                AccessToken = p.TryGetProperty("access_token", out var token) ? token.GetString() : null
            }).ToList();

            var registeredPages = _dbcontext.Organizations.ToList();

            var unregisteredPages = pages.Where(page => registeredPages.Any(x => x.FacebookId == page.Id)).ToList();

            return unregisteredPages;
        }
        public async Task<string> ExchangeForLongLivedPageToken(string pageAccessToken)
        {
            string url = $"https://graph.facebook.com/v18.0/oauth/access_token" +
                         $"?grant_type=fb_exchange_token" +
                         $"&client_id={_facebookSettings.AppId}" +
                         $"&client_secret={_facebookSettings.AppSecret}" +
                         $"&fb_exchange_token={pageAccessToken}";

            var response = await _httpClient.GetStringAsync(url);
            var json = JsonSerializer.Deserialize<JsonElement>(response);
            return json.GetProperty("access_token").GetString();
        }

        #endregion
    }
}
