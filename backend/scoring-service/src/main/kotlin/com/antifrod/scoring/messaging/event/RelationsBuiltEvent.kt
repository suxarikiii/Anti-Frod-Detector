package com.antifrod.scoring.messaging.event

data class RelationsBuiltEvent (
    val datasetId: String,
    val jobId: String,
    val usersCount: Int,
    val featuresCount: Int
)