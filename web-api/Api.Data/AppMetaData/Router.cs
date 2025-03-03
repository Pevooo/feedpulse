namespace Api.Data.AppMetaData
{
    public static class Router
    {
        public const string Root = "api";
        public const string Version = "v1";
        public const string BaseRoute = Root + "/" + Version + "/";

        public static class ApplicationUser
        {
            private const string Prefix = BaseRoute + "application-users";
            public const string Create = Prefix + "/create";
            public const string Paginated = Prefix + "/paginated";
            public const string GetById = Prefix + "/{id}";
            public const string Edit = Prefix + "/edit";
            public const string Delete = Prefix + "/{id}";
            public const string ChangePassword = Prefix + "/change-password";
        }

        public static class Authentication
        {
            private const string Prefix = BaseRoute + "authentication";
            public const string SignIn = Prefix + "/sign-in";
            public const string RefreshToken = Prefix + "/refresh-token";
            public const string ValidateToken = Prefix + "/validate-token";
            public const string ConfirmEmail = Prefix + "/confirm-email";
            public const string SendResetPasswordCode = Prefix + "/send-reset-password-code";
            public const string ConfirmResetPasswordCode = Prefix + "/confirm-reset-password-code";
            public const string ResetPassword = Prefix + "/reset-password";
        }

        public static class Authorization
        {
            private const string Prefix = BaseRoute + "authorization";
            public const string CreateRole = Prefix + "/roles/create";
            public const string EditRole = Prefix + "/roles/edit";
            public const string DeleteRole = Prefix + "/roles/delete/{id}";
            public const string RoleList = Prefix + "/roles/list";
            public const string RoleById = Prefix + "/roles/{id}";
            public const string ManageUserRole = Prefix + "/roles/manage-user-role/{id}";
            public const string UpdateUserRoles = Prefix + "/roles/update-user-roles";
            public const string UpdateUserClaims = Prefix + "/claims/update-user-claims";
            public const string ManageUserClaims = Prefix + "/claims/manage-user-claims/{id}";
        }

        public static class Emails
        {
            private const string Prefix = BaseRoute + "emails";
            public const string SendEmail = Prefix + "/send-email";
        }
        public static class Organization
        {
            private const string Prefix = BaseRoute + "emails";
            public const string Create = Prefix + "/create-organization";
        }
    }
}
