#include <stdint.h>


#define MT_N (624)
#define N             MT_N                 /* length of state vector */
#define M             (397)                /* a period parameter */
#define hiBit(u)      ((u) & 0x80000000U)  /* mask all but highest   bit of u */
#define loBit(u)      ((u) & 0x00000001U)  /* mask all but lowest    bit of u */
#define loBits(u)     ((u) & 0x7FFFFFFFU)  /* mask     the highest   bit of u */
#define mixBits(u, v) (hiBit(u)|loBits(v)) /* move hi bit of u to hi bit of v */

#define twist(m,u,v)  (m ^ (mixBits(u,v)>>1) ^ ((uint32_t)(-(int32_t)(loBit(v))) & 0x9908b0dfU))
#define twist_php(m,u,v)  (m ^ (mixBits(u,v)>>1) ^ ((uint32_t)(-(int32_t)(loBit(u))) & 0x9908b0dfU))

#define MT_RAND_MT19937 999

uint32_t mt_rand_mode = MT_RAND_MT19937;

uint32_t bg_state_val = 0;
uint32_t next_val = 0;
uint32_t * bg_state = &bg_state_val;
uint32_t * next = &next_val;
uint32_t left = 0;

/* {{{ php_mt_initialize
 */
static inline void php_mt_initialize(uint32_t seed, uint32_t *state)
{
	/* Initialize generator state with seed
	   See Knuth TAOCP Vol 2, 3rd Ed, p.106 for multiplier.
	   In previous versions, most significant bits (MSBs) of the seed affect
	   only MSBs of the state array.  Modified 9 Jan 2002 by Makoto Matsumoto. */

	register uint32_t *s = state;
	register uint32_t *r = state;
	register int i = 1;

	*s++ = seed & 0xffffffffU;
	for( ; i < N; ++i ) {
		*s++ = ( 1812433253U * ( *r ^ (*r >> 30) ) + i ) & 0xffffffffU;
		r++;
	}
}
      
static inline void php_mt_reload(void)
{
	register uint32_t *state = bg_state;
	register uint32_t *p = state;
	register int i;

	if (mt_rand_mode == MT_RAND_MT19937) {
		for (i = N - M; i--; ++p)
			*p = twist(p[M], p[0], p[1]);
		for (i = M; --i; ++p)
			*p = twist(p[M-N], p[0], p[1]);
		*p = twist(p[M-N], p[0], state[0]);
	}
	else {
		for (i = N - M; i--; ++p)
			*p = twist_php(p[M], p[0], p[1]);
		for (i = M; --i; ++p)
			*p = twist_php(p[M-N], p[0], p[1]);
		*p = twist_php(p[M-N], p[0], state[0]);
	}
	left = N;
	next = state;
}
      
void php_mt_srand(uint32_t seed)
{
	/* Seed the generator with a simple uint32 */
	php_mt_initialize(seed, bg_state);
	php_mt_reload();
	

	/* Seed only once */
	// mt_rand_is_seeded = 1;
}
      
uint32_t php_mt_rand(void)
{
	register uint32_t s1;

	// if (UNEXPECTED(!mt_rand_is_seeded)) {
	// 	php_mt_srand(GENERATE_SEED());
	// }

	if (left == 0) {
		php_mt_reload();
	}
	--left;

	s1 = *next++;
	s1 ^= (s1 >> 11);
	s1 ^= (s1 <<  7) & 0x9d2c5680U;
	s1 ^= (s1 << 15) & 0xefc60000U;

	uint32_t result = s1 ^ (s1 >> 18);
	return result >> 1;
}

