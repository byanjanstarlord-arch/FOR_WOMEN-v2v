/**
 * Three.js Hero Scene
 * Glass Orb with transmission/refraction, orbiting UI cards, energy particles, and bloom
 */

import * as THREE from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { isReducedMotion } from '../utils/reduced-motion.js';

// Card labels
const CARD_LABELS = ['Resume', 'Career', 'Skills', 'Goals', 'AI Mentor', 'Internship', 'Achievements', 'Scholarships'];
const CARD_COLORS = [
  '#7C5CFC', '#4F8CFF', '#7C5CFC', '#4F8CFF',
  '#7C5CFC', '#4F8CFF', '#7C5CFC', '#4F8CFF',
];

class HeroScene {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    if (!this.container) return;

    this.reducedMotion = isReducedMotion();
    this.isVisible = true;
    this.mouseX = 0;
    this.mouseY = 0;
    this.targetMouseX = 0;
    this.targetMouseY = 0;

    // Check if mobile
    this.isMobile = window.innerWidth < 768;
    this.orbSubdivisions = this.isMobile ? 32 : 64;
    this.particleCount = this.isMobile ? 20 : 50;
    this.cardCount = this.isMobile ? 4 : 8;
    this.useBloom = !this.isMobile;

    this.init();
  }

  init() {
    // Scene
    this.scene = new THREE.Scene();

    // Camera
    this.camera = new THREE.PerspectiveCamera(
      45,
      this.container.clientWidth / this.container.clientHeight,
      0.1,
      100
    );
    this.camera.position.set(0, 0, 5);

    // Renderer
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
    });
    this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;
    this.renderer.domElement.style.width = '100%';
    this.renderer.domElement.style.height = '100%';
    this.renderer.domElement.style.display = 'block';
    this.container.appendChild(this.renderer.domElement);

    // Post-processing (bloom)
    if (this.useBloom) {
      this.composer = new EffectComposer(this.renderer);
      this.composer.addPass(new RenderPass(this.scene, this.camera));

      const bloomPass = new UnrealBloomPass(
        new THREE.Vector2(this.container.clientWidth, this.container.clientHeight),
        0.4, // strength
        0.5, // radius
        0.85 // threshold
      );
      this.composer.addPass(bloomPass);
    }

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    this.scene.add(ambientLight);

    const mainLight = new THREE.DirectionalLight(0xffffff, 1);
    mainLight.position.set(5, 5, 5);
    this.scene.add(mainLight);

    const backLight = new THREE.DirectionalLight(0x7C5CFC, 0.5);
    backLight.position.set(-5, 3, -5);
    this.scene.add(backLight);

    const rimLight = new THREE.PointLight(0x4F8CFF, 0.8, 10);
    rimLight.position.set(0, -3, 3);
    this.scene.add(rimLight);

    // Create glass orb
    this.createOrb();

    // Create orbit cards
    this.createOrbitCards();

    // Create particles
    this.createParticles();

    // Mouse tracking
    this.container.addEventListener('mousemove', (e) => {
      const rect = this.container.getBoundingClientRect();
      this.targetMouseX = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      this.targetMouseY = -((e.clientY - rect.top) / rect.height) * 2 + 1;
    });

    // Resize handling
    window.addEventListener('resize', () => this.onResize());

    // Visibility handling
    document.addEventListener('visibilitychange', () => {
      this.isVisible = !document.hidden;
    });

    // Start animation
    this.clock = new THREE.Clock();
    this.animate();
  }

  createOrb() {
    const geometry = new THREE.IcosahedronGeometry(1, this.orbSubdivisions);

    const material = new THREE.MeshPhysicalMaterial({
      transmission: 0.98,
      thickness: 1.5,
      roughness: 0.05,
      metalness: 0.1,
      ior: 1.7,
      clearcoat: 1.0,
      clearcoatRoughness: 0.1,
      color: new THREE.Color(0xE8E0FF),
      transparent: true,
      opacity: 0.95,
    });

    // Try to set dispersion if available (Three.js r160+)
    if (material.dispersion !== undefined) {
      material.dispersion = 0.4;
    }

    this.orb = new THREE.Mesh(geometry, material);
    this.scene.add(this.orb);

    // Store initial scale for breathing animation
    this.orbBaseScale = 1;
  }

  createOrbitCards() {
    this.orbitCards = [];

    for (let i = 0; i < this.cardCount; i++) {
      // Create canvas texture for the card
      const canvas = document.createElement('canvas');
      canvas.width = 256;
      canvas.height = 160;
      const ctx = canvas.getContext('2d');

      // Glass card background
      ctx.fillStyle = 'rgba(255, 255, 255, 0.35)';
      this.roundRect(ctx, 8, 8, 240, 144, 16);
      ctx.fill();

      // Border
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
      ctx.lineWidth = 2;
      this.roundRect(ctx, 8, 8, 240, 144, 16);
      ctx.stroke();

      // Accent bar at top
      ctx.fillStyle = CARD_COLORS[i];
      ctx.beginPath();
      ctx.roundRect(24, 16, 60, 4, 2);
      ctx.fill();

      // Icon circle
      ctx.fillStyle = CARD_COLORS[i] + '20';
      ctx.beginPath();
      ctx.arc(48, 72, 20, 0, Math.PI * 2);
      ctx.fill();

      // Icon
      ctx.fillStyle = CARD_COLORS[i];
      ctx.font = 'bold 18px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(CARD_LABELS[i][0], 48, 78);

      // Label
      ctx.fillStyle = '#ffffff';
      ctx.font = '600 22px sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText(CARD_LABELS[i], 84, 78);

      const texture = new THREE.CanvasTexture(canvas);
      texture.needsUpdate = true;

      const cardGeometry = new THREE.PlaneGeometry(0.5, 0.3125);
      const cardMaterial = new THREE.MeshBasicMaterial({
        map: texture,
        transparent: true,
        opacity: 0.9,
        side: THREE.DoubleSide,
        depthWrite: false,
      });

      const card = new THREE.Mesh(cardGeometry, cardMaterial);

      // Unique orbit parameters
      const orbitParams = {
        radius: 1.4 + Math.random() * 0.8,
        speed: 0.0003 + Math.random() * 0.0005,
        tilt: (Math.random() - 0.5) * 1.0,
        phase: Math.random() * Math.PI * 2,
        card: card,
      };

      this.scene.add(card);
      this.orbitCards.push(orbitParams);
    }
  }

  roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  createParticles() {
    const particleGeometry = new THREE.SphereGeometry(1, 6, 6);
    const particleMaterial = new THREE.MeshBasicMaterial({
      color: new THREE.Color(0x7C5CFC),
      transparent: true,
      opacity: 0.3,
      depthWrite: false,
    });

    this.particles = [];

    for (let i = 0; i < this.particleCount; i++) {
      const size = 0.01 + Math.random() * 0.02;
      const mesh = new THREE.Mesh(particleGeometry, particleMaterial.clone());

      mesh.scale.setScalar(size);
      mesh.position.set(
        (Math.random() - 0.5) * 6,
        (Math.random() - 0.5) * 4,
        (Math.random() - 0.5) * 3
      );

      const particle = {
        mesh: mesh,
        seed: Math.random() * 100,
        basePosition: mesh.position.clone(),
      };

      this.scene.add(mesh);
      this.particles.push(particle);
    }
  }

  onResize() {
    if (!this.container || !this.camera || !this.renderer) return;

    const width = this.container.clientWidth;
    const height = this.container.clientHeight;

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();

    this.renderer.setSize(width, height);

    if (this.composer) {
      this.composer.setSize(width, height);
    }
  }

  animate() {
    if (!this.isVisible) {
      requestAnimationFrame(() => this.animate());
      return;
    }

    const time = this.clock.getElapsedTime();

    // Lerp mouse
    this.mouseX += (this.targetMouseX - this.mouseX) * 0.05;
    this.mouseY += (this.targetMouseY - this.mouseY) * 0.05;

    if (!this.reducedMotion) {
      // Orb rotation
      this.orb.rotation.y += 0.001 + Math.abs(this.mouseX) * 0.002;

      // Orb tilt toward mouse
      this.orb.rotation.x += (this.mouseY * 0.15 - this.orb.rotation.x) * 0.05;
      this.orb.rotation.z += (this.mouseX * 0.1 - this.orb.rotation.z) * 0.05;

      // Breathing animation
      const breathe = Math.sin(time * 0.8) * 0.02 + 1;
      this.orb.scale.setScalar(this.orbBaseScale * breathe);

      // Update orbit cards
      const mouseShiftX = this.mouseX * 0.3;
      const mouseShiftY = this.mouseY * 0.3;

      this.orbitCards.forEach((params) => {
        const t = time * params.speed * 60 + params.phase;

        // Elliptical orbit
        let x = Math.cos(t) * params.radius + mouseShiftX;
        let y = Math.sin(t * 0.7) * params.radius * 0.6 + mouseShiftY;
        let z = Math.sin(t) * params.radius * 0.4;

        // Apply tilt
        const cosTilt = Math.cos(params.tilt);
        const sinTilt = Math.sin(params.tilt);
        const yT = y * cosTilt - z * sinTilt;
        const zT = y * sinTilt + z * cosTilt;

        params.card.position.set(x, yT, zT);
        params.card.lookAt(this.camera.position);

        // Opacity pulse
        params.card.material.opacity =
          0.7 + Math.sin(time * 2 + params.phase) * 0.15;
      });

      // Update particles
      this.particles.forEach((p) => {
        p.mesh.position.x =
          p.basePosition.x + Math.sin(time * 0.1 + p.seed) * 0.3;
        p.mesh.position.y =
          p.basePosition.y + Math.cos(time * 0.08 + p.seed) * 0.2;
        p.mesh.position.z =
          p.basePosition.z + Math.sin(time * 0.12 + p.seed) * 0.15;

        p.mesh.material.opacity =
          0.15 + Math.sin(time * 0.5 + p.seed) * 0.1;
      });
    }

    // Render
    if (this.composer) {
      this.composer.render();
    } else {
      this.renderer.render(this.scene, this.camera);
    }

    requestAnimationFrame(() => this.animate());
  }

  dispose() {
    this.isVisible = false;

    // Dispose geometries
    this.orb.geometry.dispose();
    this.orb.material.dispose();

    this.orbitCards.forEach((params) => {
      params.card.geometry.dispose();
      params.card.material.map.dispose();
      params.card.material.dispose();
    });

    this.particles.forEach((p) => {
      p.mesh.geometry.dispose();
      p.mesh.material.dispose();
    });

    this.renderer.dispose();
    if (this.composer) this.composer.dispose();

    if (this.container && this.renderer.domElement) {
      this.container.removeChild(this.renderer.domElement);
    }
  }
}

export function initHeroScene() {
  return new HeroScene('hero-canvas-container');
}

export default HeroScene;
