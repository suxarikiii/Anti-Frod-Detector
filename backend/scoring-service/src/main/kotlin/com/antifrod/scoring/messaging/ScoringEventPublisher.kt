package com.antifrod.scoring.messaging

import org.springframework.amqp.rabbit.core.RabbitTemplate
import org.springframework.stereotype.Component

@Component
class ScoringEventPublisher(
    private val rabbitTemplate: RabbitTemplate
) {

    fun publishScoringCompleted(event: ScoringCompletedEvent) {
        rabbitTemplate.convertAndSend(
            "pipeline.exchange",
            "scoring.completed",
            event
        )
    }

    fun publishPipelineFailed(event: PipelineFailedEvent) {
        rabbitTemplate.convertAndSend(
            "pipeline.exchange",
            "pipeline.failed",
            event
        )
    }
}