package com.antifrod.scoring.model


data class SuspiciousUser (
    val userId: String,
    val riskScore: Int,
    val riskLevel: RiskLevel,
    val topReason: String,
    val relatedUsersCount: Int
)