
#version 130

in vec2 iPosition;
in vec2 iVelocity;
in uint iSeed;

out vec2 oPosition;
out vec2 oVelocity;
flat out uint oSeed;

uint seed;

const float M_TAU = 6.28318530718;
const float InverseMaxInt = 1.0 / 4294967295.0;

float randhash(float b)
{
  uint i = (seed ^ 12345391u) * 2654435769u;
  i ^= (i << 6u) ^ (i >> 26u);
  i *= 2654435769u;
  seed = i;
  i += (i << 5u) ^ (i >> 12u);
  return float(b * i) * InverseMaxInt;
}

void main()
{
  seed = iSeed;

  if (dot(iPosition, iPosition) > 100.00)
  {
    float theta = randhash(M_TAU);
    oPosition = vec2(0, 0);
    oVelocity = 0.01 * vec2(cos(theta), sin(theta));
  }
  else
  {
    oPosition = iPosition + iVelocity;
    oVelocity = iVelocity;
  }

  float t = gl_VertexID / 10000.0;
  gl_Position.xy = iPosition;
  gl_Position.z = 0;
  gl_Position.w = 1;

  oPosition = vec2(t,t);

  oSeed = seed;
}
