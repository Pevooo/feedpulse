namespace Api.Core.Features.Users.Queries.Response
{
    public class GetUserListResponse
    {
        public string FullName { get; set; }
        public string Email { get; set; }
        public string? Address { get; set; }
        public string? Country { get; set; }
        public string? Description { get; set; }
    }
}
