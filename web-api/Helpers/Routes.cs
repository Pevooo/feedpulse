namespace web_api.Helpers
{
    public static class Routes
    {
        public const string SignleRoute = "/{id}";

        public const string root = "Api";
        public const string version = "V1";
        public const string Rule = root + "/" + version + "/";
        public static class CategoryRouting
        {
            public const string Prefix = Rule + "Category";
            public const string List = Prefix + "/List";

        }
        public static class AuthRouting
        {
            public const string Prefix = Rule + "Auth";
            public const string Login = Prefix + "/Login";
            public const string Register = Prefix + "/Register";
            public const string RefershToken = Prefix + "/RefreshToken";
            public const string RevokeToken = Prefix + "/RevokeToken";


        }
    }
}
