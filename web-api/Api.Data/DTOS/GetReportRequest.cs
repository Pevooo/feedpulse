using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Data.DTOS
{
	public class GetReportRequest
	{
		public string page_id { get; set; }
		public DateTime start_date { get; set; }
		public DateTime end_date { get; set; }
	}
}
