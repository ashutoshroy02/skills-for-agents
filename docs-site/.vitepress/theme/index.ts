import DefaultTheme from 'vitepress/theme'
import './custom.css'
import { h } from 'vue'

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      'layout-top': () => h('a', {
        href: '#VPContent',
        class: 'skip-link',
        innerHTML: 'Skip to main content'
      }),
      'home-hero-before': () => h('div', {
        class: 'hero-waves',
        innerHTML: `
          <svg class="wave-bg" viewBox="0 0 1200 400" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
            <defs>
              <linearGradient id="waveGrad1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:oklch(65% 0.20 280 / 0.15)" />
                <stop offset="50%" style="stop-color:oklch(70% 0.22 260 / 0.15)" />
                <stop offset="100%" style="stop-color:oklch(65% 0.20 280 / 0.15)" />
              </linearGradient>
              <linearGradient id="waveGrad2" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:oklch(70% 0.22 260 / 0.10)" />
                <stop offset="50%" style="stop-color:oklch(65% 0.20 280 / 0.10)" />
                <stop offset="100%" style="stop-color:oklch(70% 0.22 260 / 0.10)" />
              </linearGradient>
            </defs>
            <path d="M0,200 Q300,150 600,200 T1200,200 L1200,400 L0,400 Z" fill="url(#waveGrad1)">
              <animate attributeName="d" 
                dur="10s" 
                repeatCount="indefinite"
                values="
                  M0,200 Q300,150 600,200 T1200,200 L1200,400 L0,400 Z;
                  M0,200 Q300,250 600,200 T1200,200 L1200,400 L0,400 Z;
                  M0,200 Q300,150 600,200 T1200,200 L1200,400 L0,400 Z
                "
              />
            </path>
            <path d="M0,240 Q300,200 600,240 T1200,240 L1200,400 L0,400 Z" fill="url(#waveGrad2)">
              <animate attributeName="d" 
                dur="8s" 
                repeatCount="indefinite"
                values="
                  M0,240 Q300,200 600,240 T1200,240 L1200,400 L0,400 Z;
                  M0,240 Q300,280 600,240 T1200,240 L1200,400 L0,400 Z;
                  M0,240 Q300,200 600,240 T1200,240 L1200,400 L0,400 Z
                "
              />
            </path>
          </svg>
        `
      })
    })
  }
}


