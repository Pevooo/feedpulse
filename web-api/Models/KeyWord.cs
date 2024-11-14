namespace web_api.Models
{
    public class KeyWord
    {
        public int KeyWordId { get; set; }

        public string Keyword { get; set; }


        public Organization Organization { get; set; }
    }
}
