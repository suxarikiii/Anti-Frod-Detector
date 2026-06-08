package com.antifrod.scoring.model

import java.time.Instant

data class RiskScore (
    val userId: String,
    val datasetId: String,
    val score: Int,
    val riskLevel: RiskLevel,
    val reasons: List<RiskReason>,
    val calculatedAt: Instant
)