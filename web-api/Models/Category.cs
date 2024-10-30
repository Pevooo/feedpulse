namespace web_api.Models
{
    public class Category
    {
        public int CategoryId { get; set; }
        public string PlatformName { get; set; }= string.Empty;
        public IEnumerable<ORGSocial> URlS { get; set; }
    }
}
