namespace Api.Data.Helpers
{
    public class JWTAuthRes
    {
        public string AccessToken { get; set; }
        public RefreshToken RefreshToken { get; set; }

    }
    public class RefreshToken
    {
        public string UserName { get; set; }
        public string Token { get; set; }
        public DateTime Expireat { get; set; }


    }
}
