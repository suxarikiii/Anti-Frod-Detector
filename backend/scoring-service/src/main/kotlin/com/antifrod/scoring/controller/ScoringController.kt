package com.antifrod.scoring.controller

import com.antifrod.scoring.model.RecalculateResponse
import com.antifrod.scoring.model.RiskScore
import com.antifrod.scoring.model.SuspiciousUser
import com.antifrod.scoring.service.ScoringService
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.PathVariable
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

@RestController
@RequestMapping("/api/scoring")
class ScoringController(
    private val scoringService: ScoringService
) {

    @GetMapping("/datasets/{datasetId}/suspicious-users")
    fun getSuspiciousUsers(
        @PathVariable datasetId: String
    ): List<SuspiciousUser> {
        return scoringService.getSuspiciousUsers(datasetId)
    }

    @GetMapping("/users/{userId}/risk")
    fun getUserRisk(
        @PathVariable userId: String
    ): RiskScore {
        return scoringService.getUserRisk(userId)
    }

    @PostMapping("/datasets/{datasetId}/recalculate")
    fun recalculateDataset(
        @PathVariable datasetId: String
    ): RecalculateResponse {
        return scoringService.recalculateDataset(datasetId)
    }
}