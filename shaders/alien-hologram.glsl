// Alien Glyphs — alien-hologram.glsl
// Ghostty custom shader (Shadertoy format: mainImage, uniforms provided by Ghostty).
// UFO hologram vibes: mint-green glow, subtle scanlines, gentle flicker,
// vignette, slight chromatic fringe, and a slow hologram sweep band.
// Tuned to stay readable for daily terminal use: no UV distortion, no blur
// applied to the base text — glow is additive only around bright pixels.
//
// Enable in ~/.config/ghostty/config:
//   custom-shader = shaders/alien-hologram.glsl
// (path relative to the Ghostty config directory, or use an absolute path)

void mainImage(out vec4 fragColor, in vec2 fragCoord)
{
    vec2 uv = fragCoord / iResolution.xy;
    vec2 px = 1.0 / iResolution.xy;

    // --- Base + cheap glow bloom (additive, text itself is untouched) ---
    vec4 base = texture(iChannel0, uv);

    // 8-tap small-radius blur, only used as an additive glow source.
    vec3 blur = vec3(0.0);
    blur += texture(iChannel0, uv + vec2( 1.5,  0.0) * px).rgb;
    blur += texture(iChannel0, uv + vec2(-1.5,  0.0) * px).rgb;
    blur += texture(iChannel0, uv + vec2( 0.0,  1.5) * px).rgb;
    blur += texture(iChannel0, uv + vec2( 0.0, -1.5) * px).rgb;
    blur += texture(iChannel0, uv + vec2( 1.0,  1.0) * px).rgb;
    blur += texture(iChannel0, uv + vec2(-1.0,  1.0) * px).rgb;
    blur += texture(iChannel0, uv + vec2( 1.0, -1.0) * px).rgb;
    blur += texture(iChannel0, uv + vec2(-1.0, -1.0) * px).rgb;
    blur /= 8.0;

    float luminance = dot(blur, vec3(0.299, 0.587, 0.114));
    float bright = smoothstep(0.18, 0.85, luminance);
    vec3 mint = vec3(0.486, 1.0, 0.698); // #7CFFB2
    vec3 glow = blur * bright * 0.55 + mint * bright * 0.12;

    vec3 color = base.rgb + glow;

    // --- Slight chromatic fringe on bright areas (1px R/B split) ---
    float fringe = bright * 0.75;
    color.r += texture(iChannel0, uv + vec2( 1.0, 0.0) * px).r * fringe * 0.18;
    color.b += texture(iChannel0, uv + vec2(-1.0, 0.0) * px).b * fringe * 0.18;

    // --- Dark background tint: near-black, faint green ---
    float darkness = 1.0 - smoothstep(0.0, 0.22, dot(base.rgb, vec3(0.333)));
    color = mix(color, vec3(0.008, 0.016, 0.008), darkness * 0.35);

    // --- Subtle scanlines ---
    float scan = 0.97 + 0.03 * sin(fragCoord.y * 3.14159265);
    color *= scan;

    // --- Gentle flicker (slow + tiny fast component, both very small) ---
    float flicker = 0.985
        + 0.010 * sin(iTime * 7.3)
        + 0.005 * sin(iTime * 31.7 + 1.7);
    color *= flicker;

    // --- Occasional hologram sweep band (slow, faint) ---
    float bandPos = fract(iTime * 0.045);
    float band = exp(-pow((uv.y - bandPos) * 14.0, 2.0));
    color += mint * band * 0.045;

    // Very faint second static interference line pattern, kept extremely low.
    color += mint * 0.012 * smoothstep(0.92, 1.0, sin(uv.y * 220.0 + iTime * 0.7) * 0.5 + 0.5);

    // --- Soft cursor halo (only when cursor is visible) ---
    if (iCursorVisible == 1) {
        // iCurrentCursor: (x, y, width, height) in pixels, y top-down; flip to fragCoord space.
        vec2 cmin = vec2(iCurrentCursor.x, iResolution.y - iCurrentCursor.y - iCurrentCursor.w);
        vec2 cmax = vec2(iCurrentCursor.x + iCurrentCursor.z, iResolution.y - iCurrentCursor.y);
        vec2 d = max(max(cmin - fragCoord, fragCoord - cmax), vec2(0.0));
        float dist = length(d);
        color += mint * exp(-dist * 0.08) * 0.08;
    }

    // --- Vignette ---
    vec2 centered = uv - 0.5;
    float vignette = 1.0 - dot(centered, centered) * 0.55;
    color *= clamp(vignette, 0.72, 1.0);

    fragColor = vec4(color, base.a);
}
