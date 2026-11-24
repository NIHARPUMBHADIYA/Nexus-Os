#version 450
// KWin 6 Rounded Corners Composite Fragment Shader
// Clips client window buffers to radius-lg (16px) with 1.5px sub-pixel anti-aliasing.

layout(location = 0) in vec2 v_texCoord;
layout(location = 0) out vec4 fragColor;

layout(binding = 0) uniform sampler2D u_texture;

layout(push_constant) uniform WindowUniforms {
    vec2 windowSize;
    float cornerRadius; // default: 16.0
} u_window;

void main() {
    vec2 halfSize = u_window.windowSize * 0.5;
    vec2 p = abs(gl_FragCoord.xy - halfSize) - (halfSize - vec2(u_window.cornerRadius));
    float dist = length(max(p, 0.0)) + min(max(p.x, p.y), 0.0) - u_window.cornerRadius;

    // Sub-pixel edge anti-aliasing
    float alpha = clamp(0.5 - dist, 0.0, 1.0);

    vec4 texColor = texture(u_texture, v_texCoord);
    fragColor = texColor * alpha;
}
