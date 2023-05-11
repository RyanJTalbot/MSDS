package io.collective

import java.time.Clock

class SimpleAgedKache {
    constructor(clock: Clock?) {
    }

    constructor() {
    }

    fun put(key: Any?, value: Any?, retentionInMillis: Int) {

    }

    fun isEmpty(): Boolean {
        return false
    }

    fun size(): Int {
        return 0
    }

    fun get(key: Any?): Any? {
        return null
    }
}