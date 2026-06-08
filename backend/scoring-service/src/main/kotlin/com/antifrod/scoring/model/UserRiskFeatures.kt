package com.antifrod.scoring.model

data class UserRiskFeatures(
    val sameDeviceUserCount: Int,
    val sameIpUserCount: Int,
    val promoUsageCount: Int,
    val hasSuspiciousReferral: Boolean
)