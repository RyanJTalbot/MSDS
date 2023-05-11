package test.collective

import io.collective.SimpleAgedKache
import junit.framework.TestCase.*
import org.junit.Before
import org.junit.Ignore
import java.time.Clock
import java.time.Duration
import java.time.Instant
import java.time.ZoneId

class SimpleAgedKacheTest {
    var empty = SimpleAgedKache()
    var nonempty = SimpleAgedKache()

    @Before
    fun before() {
        nonempty.put("aKey", "aValue", 2000)
        nonempty.put("anotherKey", "anotherValue", 4000)
    }

    @Ignore
    fun isEmpty() {
        assertTrue(empty.isEmpty())
        assertFalse(nonempty.isEmpty())
    }

    @Ignore
    fun size() {
        assertEquals(0, empty.size())
        assertEquals(2, nonempty.size())
    }

    @Ignore
    fun get() {
        assertNull(empty.get("aKey"))
        assertEquals("aValue", nonempty.get("aKey"))
        assertEquals("anotherValue", nonempty.get("anotherKey"))
    }

    @Ignore
    fun getExpired() {
        val clock = TestClock()
        val expired = SimpleAgedKache(clock)
        expired.put("aKey", "aValue", 2000)
        expired.put("anotherKey", "anotherValue", 4000)
        clock.offset(Duration.ofMillis(3000))
        assertEquals(1, expired.size())
        assertEquals("anotherValue", expired.get("anotherKey"))
    }

    internal class TestClock : Clock() {
        var offset = Duration.ZERO

        override fun getZone(): ZoneId {
            return systemDefaultZone().zone
        }

        override fun withZone(zone: ZoneId): Clock {
            return offset(system(zone), offset)
        }

        override fun instant(): Instant {
            return offset(systemDefaultZone(), offset).instant()
        }

        fun offset(offset: Duration) {
            this.offset = offset
        }
    }
}