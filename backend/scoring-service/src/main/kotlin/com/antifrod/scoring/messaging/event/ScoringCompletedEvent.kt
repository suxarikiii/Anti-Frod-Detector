package com.antifrod.scoring.messaging.event

import java.time.Instant

data class ScoringCompletedEvent (
    val datasetId: String,
    val jobId: String,
    val scoredUsersCount: Int,
    val suspiciousUsersCount: Int,
    val publishedAt: Instant
)