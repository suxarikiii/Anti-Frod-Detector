package com.antifrod.scoring.messaging.event

import java.time.Instant

data class PipelineFailedEvent(
    val datasetId: String,
    val jobId: String,
    val failedStage: String,
    val message: String,
    val publishedAt: Instant
)