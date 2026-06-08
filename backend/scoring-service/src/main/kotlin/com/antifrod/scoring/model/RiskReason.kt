package com.antifrod.scoring.model

data class RiskReason(
    val type: String,
    val message: String,
    val scoreImpact: Int
)