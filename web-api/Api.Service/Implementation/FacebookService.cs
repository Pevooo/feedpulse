using Api.Data.Helpers;
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
        #endregion

        #region Constructor
        public FacebookService(IOptions<FacebookSettings> facebookSettings, HttpClient httpClient)
        {
            _facebookSettings = facebookSettings.Value;
            _httpClient = httpClient;
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

        #endregion
    }
}
