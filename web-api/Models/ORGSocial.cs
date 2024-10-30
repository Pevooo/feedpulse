namespace web_api.Models
{
    public class ORGSocial
    {
        public int ORGSocialId { get; set; }
        public string Url { get; set; }= string.Empty;
        public Category Category { get; set; }
        public Organization Organization { get; set; }
    }
}
