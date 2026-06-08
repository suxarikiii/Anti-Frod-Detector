package com.antifrod.scoring.config

import org.springframework.amqp.core.DirectExchange
import org.springframework.amqp.core.Queue
import org.springframework.amqp.core.Binding
import org.springframework.amqp.core.BindingBuilder
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration


@Configuration
class RabbitMqConfig {
    @Bean
    fun pipelineExchange(): DirectExchange {
        return DirectExchange("pipeline.exchange")
    }

    @Bean
    fun relationsBuiltQueue(): Queue {
        return Queue("scoring.relations-built.queue", true)
    }

    @Bean
    fun relationsBuiltBinding(
        relationsBuiltQueue: Queue,
        pipelineExchange: DirectExchange
    ): Binding {
        return BindingBuilder
            .bind(relationsBuiltQueue)
            .to(pipelineExchange)
            .with("relations.built")
    }
}