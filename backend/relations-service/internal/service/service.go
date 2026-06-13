package service

import (
	"context"
	"fmt"
	"time"

	"relations-service/internal/domain"
)

type RelationsBuiltPublisher interface {
	PublishRelationsBuilt(ctx context.Context, event RelationsBuiltEvent) error
}

type Service struct {
	publisher RelationsBuiltPublisher
}

type NormalizedDatasetEvent struct {
	DatasetID   string `json:"datasetId"`
	JobID       string `json:"jobId"`
	RecordsPath string `json:"recordsPath,omitempty"`
	PublishedAt string `json:"publishedAt,omitempty"`
}

type RelationsBuiltEvent struct {
	DatasetID     string `json:"datasetId"`
	JobID         string `json:"jobId"`
	ReturnsCount  int    `json:"returnsCount"`
	FeaturesCount int    `json:"featuresCount"`
	PublishedAt   string `json:"publishedAt"`
}

func NewService(publisher RelationsBuiltPublisher) *Service {
	return &Service{publisher: publisher}
}

func (s *Service) Health() map[string]string {
	return map[string]string{
		"status":  "UP",
		"service": "relations-service",
	}
}

func (s *Service) RebuildDataset(ctx context.Context, datasetID string) (*domain.DatasetRebuildResponse, error) {
	jobID := fmt.Sprintf("relations-job-%s", datasetID)
	if err := s.publishRelationsBuilt(ctx, datasetID, jobID); err != nil {
		return nil, err
	}

	return &domain.DatasetRebuildResponse{
		DatasetID: datasetID,
		JobID:     jobID,
		Status:    "RELATIONS_REBUILD_STARTED",
	}, nil
}

func (s *Service) ProcessNormalizedDataset(ctx context.Context, event NormalizedDatasetEvent) error {
	return s.publishRelationsBuilt(ctx, event.DatasetID, event.JobID)
}

func (s *Service) GetReturnRelations(returnID string) *domain.ReturnRelations {
	return &domain.ReturnRelations{
		ReturnID:        returnID,
		CustomerID:      "customer_789",
		OrderID:         "order_456",
		SupportAgentID:  "agent_001",
		ProductCategory: "electronics",
		Decision: domain.SupportDecision{
			DecisionID:     "decision_321",
			Status:         "approved",
			RefundAmount:   249.90,
			ManualOverride: true,
			DecisionTimeMs: 4300,
		},
		Relations: []domain.GraphRelation{
			{From: "customer_789", Type: "PLACED_ORDER", To: "order_456"},
			{From: "order_456", Type: "HAS_RETURN_REQUEST", To: returnID},
			{From: returnID, Type: "DECIDED_BY", To: "agent_001"},
			{From: "order_456", Type: "HAS_CATEGORY", To: "electronics"},
			{From: "agent_001", Type: "MADE_DECISION", To: "decision_321"},
			{From: "decision_321", Type: "APPROVED_RETURN", To: returnID},
		},
	}
}

func (s *Service) GetCustomerHistory(customerID string) *domain.CustomerHistory {
	return &domain.CustomerHistory{
		CustomerID:      customerID,
		OrdersCount:     14,
		ReturnCount:     8,
		ApprovedRefunds: 6,
		RecentReturns: []domain.ReturnListItem{
			{
				ReturnID:       "return_123",
				OrderID:        "order_456",
				Reason:         "item_not_as_described",
				Category:       "electronics",
				RefundAmount:   249.90,
				DecisionStatus: "approved",
				SupportAgentID: "agent_001",
			},
			{
				ReturnID:       "return_124",
				OrderID:        "order_457",
				Reason:         "damaged_item",
				Category:       "electronics",
				RefundAmount:   199.50,
				DecisionStatus: "approved",
				SupportAgentID: "agent_001",
			},
		},
		LinkedAgents: []domain.LinkedAgent{
			{SupportAgentID: "agent_001", PairCount: 5},
			{SupportAgentID: "agent_014", PairCount: 2},
		},
	}
}

func (s *Service) GetAgentSummary(agentID string) *domain.AgentSummary {
	return &domain.AgentSummary{
		SupportAgentID:            agentID,
		DecisionsCount:            118,
		ApprovalRate:              0.91,
		HighValueApprovalCount:    14,
		ManualOverrideCount:       9,
		RepeatedCustomerPairCount: 5,
		TopRiskyCategory:          "electronics",
	}
}

func (s *Service) GetReturnFeatures(returnID string) *domain.ReturnFeaturesResponse {
	return &domain.ReturnFeaturesResponse{
		ReturnID:       returnID,
		CustomerID:     "customer_789",
		SupportAgentID: "agent_001",
		Features: domain.RelationFeatures{
			CustomerReturnCount:         8,
			CustomerApprovedRefundCount: 6,
			AgentApprovalRate:           0.91,
			AgentHighValueApprovalCount: 14,
			CustomerAgentPairCount:      5,
			CategoryRefundRate:          0.27,
			SimilarReturnsCount:         4,
			ClusterSize:                 9,
		},
	}
}

func (s *Service) publishRelationsBuilt(ctx context.Context, datasetID, jobID string) error {
	if s.publisher == nil {
		return nil
	}

	return s.publisher.PublishRelationsBuilt(ctx, RelationsBuiltEvent{
		DatasetID:     datasetID,
		JobID:         jobID,
		ReturnsCount:  42,
		FeaturesCount: 42,
		PublishedAt:   time.Now().UTC().Format(time.RFC3339),
	})
}
