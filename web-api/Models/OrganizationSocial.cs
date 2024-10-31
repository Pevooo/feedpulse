namespace web_api.Models
{
    public class OrganizationSocial
    {
        public int OrganizationSocialId { get; set; }
        public string Url { get; set; } = string.Empty;
        public Category Category { get; set; }
        public Organization Organization { get; set; }
    }
}
