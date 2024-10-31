namespace web_api.Models
{
    public class Report
    {
        public int ReportId { get; set; }
        public string ReportName { get; set; } = string.Empty;
        public byte[] FileData { get; set; }
        public DateTime Date { get; set; }
        public Organization Organization { get; set; }
    }
}
