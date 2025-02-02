namespace Api.Data.DTOS
{
    public class ManageUserRolesResponse
    {
        public string UserId { get; set; }
        public List<Role> Roles { get; set; }

    }
    public class Role
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public bool HasRole { get; set; } = false;
    }
}
