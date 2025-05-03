using Api.Core.Bases;
using Api.Core.Features.Organizations.Queries.Models;
using Api.Core.Features.Organizations.Queries.Responses;
using Api.Data.DTOS;
using Api.Service.Abstracts;
using AutoMapper;
using MediatR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Api.Core.Features.Organizations.Queries.Handler
{

    public class OrganizationQueryHandler : ResponseHandler, IRequestHandler<GetOrganizationListQuery, Response<List<GetOrganizationResponse>>>
                            , IRequestHandler<GetOrganizationQuery, Response<GetOrganizationResponse>>,
						IRequestHandler<GetReportQuery, Response<GetReportResponse>>
    {
        #region Fields
        IOrganizationService _organizationService;
        IMapper _mapper;
        #endregion
        #region Constructor
        public OrganizationQueryHandler(IOrganizationService organizationService, IMapper mapper)
        {
            _organizationService = organizationService;
            _mapper = mapper;
        }
        #endregion
        #region HandleFunctions
        public async Task<Response<List<GetOrganizationResponse>>> Handle(GetOrganizationListQuery request, CancellationToken cancellationToken)
        {
            var organizations = await _organizationService.GetOrganizationsByUseridAsync(request.UserId);
            var response = organizations.Select(o => new GetOrganizationResponse
            {
                Name = o.Name,
                Description = o.Description,
                FacebookId = o.FacebookId,
                PageAccessToken = o.PageAccessToken
            }).ToList();

            return Success(response);
        }

        public async Task<Response<GetOrganizationResponse>> Handle(GetOrganizationQuery request, CancellationToken cancellationToken)
        {
            var organization = await _organizationService.GetOrganizationByIdAsync(request.OrganizationId);
            var response = new GetOrganizationResponse
            {
                Name = organization.Name,
                Description = organization.Description,
                FacebookId = organization.FacebookId,
                PageAccessToken = organization.PageAccessToken
            };
            return Success(response);
        }
		public async Task<Response<GetReportResponse>> Handle(GetReportQuery request, CancellationToken cancellationToken)
		{
            var req = new GetReportRequest
            {
                page_id = request.page_id,
                start_date = request.start_date,
                end_date = request.end_date
            };
            var report = await _organizationService.GetReportAsync(req);
            var response = new GetReportResponse
            {
				Body = new ReportResponseBody
				{
					ChartRasters = report.Body.ChartRasters.ToList(),
					Goals = report.Body.Goals.ToList(),
					Metrics = new ReportResponseMetrics
					{
						MostFreqSentimentPerTopic = new Dictionary<string, string>(report.Body.Metrics.MostFreqSentimentPerTopic),
						MostFreqTopicPerSentiment = new Dictionary<string, string>(report.Body.Metrics.MostFreqTopicPerSentiment),
						SentimentCounts = new Dictionary<string, int>(report.Body.Metrics.SentimentCounts),
						Top5Topics = new Dictionary<string, int>(report.Body.Metrics.Top5Topics),
						TopicCounts = new Dictionary<string, int>(report.Body.Metrics.TopicCounts)
					},
					Summary = report.Body.Summary
				},
				Status = report.Status
			};

			return Success(response);
		}
		#endregion
	}
}
