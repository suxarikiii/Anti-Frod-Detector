package com.antifrod.scoring.service

import com.antifrod.scoring.model.RecalculateResponse
import com.antifrod.scoring.model.RiskLevel
import com.antifrod.scoring.model.RiskReason
import com.antifrod.scoring.model.RiskScore
import com.antifrod.scoring.model.SuspiciousUser
import org.springframework.stereotype.Service
import java.time.Instant

@Service
class ScoringService {

    fun getSuspiciousUsers(datasetId: String): List<SuspiciousUser> {
        return listOf(
            SuspiciousUser(
                userId = "user_123",
                riskScore = 87,
                riskLevel = RiskLevel.HIGH,
                topReason = "Same device used by 5 users",
                relatedUser = 6
            ),
            SuspiciousUser(
                userId = "user_456",
                riskScore = 64,
                riskLevel = RiskLevel.MEDIUM,
                topReason = "Same IP used by 3 users",
                relatedUser = 3
            ),
            SuspiciousUser(
                userId = "user_789",
                riskScore = 35,
                riskLevel = RiskLevel.LOW,
                topReason = "Promo usage count is above normal",
                relatedUser = 1
            )
        )
    }

    fun getUserRisk(userId: String): RiskScore {
        val datasetId = "demo"

        val reasons = mockReasonsForUser(userId)
        val score = reasons.sumOf { it.scoreImpact }.coerceIn(0, 100)

        return RiskScore(
            userId = userId,
            datasetId = datasetId,
            score = score,
            riskLevel = resolveRiskLevel(score),
            reasons = reasons,
            calculatedAt = Instant.now()
        )
    }

    fun recalculateDataset(datasetId: String): RecalculateResponse {
        return RecalculateResponse(
            datasetId = datasetId,
            status = "RECALCULATION_STARTED"
        )
    }

    private fun mockReasonsForUser(userId: String): List<RiskReason> {
        return when (userId) {
            "user_123" -> listOf(
                RiskReason(
                    type = "SAME_DEVICE",
                    message = "Same device used by 5 users",
                    scoreImpact = 30
                ),
                RiskReason(
                    type = "SAME_IP",
                    message = "Same IP used by 3 users",
                    scoreImpact = 20
                ),
                RiskReason(
                    type = "PROMO_ABUSE",
                    message = "User used promo code 5 times",
                    scoreImpact = 20
                ),
                RiskReason(
                    type = "SUSPICIOUS_REFERRAL",
                    message = "User has suspicious referral relation",
                    scoreImpact = 30
                )
            )

            "user_456" -> listOf(
                RiskReason(
                    type = "SAME_IP",
                    message = "Same IP used by 3 users",
                    scoreImpact = 20
                ),
                RiskReason(
                    type = "PROMO_ABUSE",
                    message = "User used promo code 5 times",
                    scoreImpact = 20
                )
            )

            else -> listOf(
                RiskReason(
                    type = "PROMO_ABUSE",
                    message = "User has repeated promo usage",
                    scoreImpact = 20
                )
            )
        }
    }

    private fun resolveRiskLevel(score: Int): RiskLevel {
        return when {
            score >= 70 -> RiskLevel.HIGH
            score >= 40 -> RiskLevel.MEDIUM
            else -> RiskLevel.LOW
        }
    }
}