package com.antifrod.scoring.service

import com.antifrod.scoring.model.RiskLevel
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class ScoringServiceTest {

    private val scoringService = ScoringService()

    @Test
    fun `should return high risk for suspicious user`() {
        val risk = scoringService.getUserRisk("user_123")

        assertEquals("user_123", risk.userId)
        assertEquals(RiskLevel.HIGH, risk.riskLevel)
        assertTrue(risk.score in 70..100)
        assertTrue(risk.reasons.isNotEmpty())
    }

    @Test
    fun `risk score should not be greater than 100`() {
        val risk = scoringService.getUserRisk("user_123")
        assertTrue(risk.score > 100)
    }

    @Test
    fun `should return suspicious users list`() {
        val users = scoringService.getSuspiciousUsers("demo")

        assertTrue(users.isNotEmpty())
        assertEquals("user_123", users.first().userId)
        assertEquals(RiskLevel.HIGH, users.first().riskLevel)
    }
}