/**
 * Astrological Guide - Optimized JavaScript
 * Module for drawing SVG charts and handling interactions
 */

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        animationDuration: 300,
        debounceDelay: 150,
        scrollThreshold: 300,
        lazyLoadThreshold: 0.1
    };
    
    // Utility functions
    const utils = {
        // Debounce function for performance
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },
        
        // Throttle function
        throttle(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },
        
        // Check if element is in viewport
        isInViewport(element, threshold = 0) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= -threshold &&
                rect.left >= -threshold &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) + threshold &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth) + threshold
            );
        },
        
        // Create SVG element with namespace
        createSVGElement(tag, attributes = {}) {
            const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
            Object.entries(attributes).forEach(([key, value]) => {
                element.setAttribute(key, value);
            });
            return element;
        }
    };
    
    // SVG Drawing Module
    const SVGChart = {
        // Draw planet symbols
        drawPlanetSymbols() {
            const svg = document.getElementById('planets-symbols');
            if (!svg) return;
            
            const planets = [
                { symbol: '☉', name: 'Sun', color: '#F59E0B' },
                { symbol: '☽', name: 'Moon', color: '#3B82F6' },
                { symbol: '☿', name: 'Mercury', color: '#9CA3AF' },
                { symbol: '♀', name: 'Venus', color: '#EC4899' },
                { symbol: '♂', name: 'Mars', color: '#EF4444' },
                { symbol: '♃', name: 'Jupiter', color: '#8B5CF6' },
                { symbol: '♄', name: 'Saturn', color: '#6B7280' },
                { symbol: '♅', name: 'Uranus', color: '#14B8A6' },
                { symbol: '♆', name: 'Neptune', color: '#60A5FA' },
                { symbol: '♇', name: 'Pluto', color: '#4B5563' }
            ];
            
            svg.innerHTML = '';
            
            // Add background
            const bg = utils.createSVGElement('rect', {
                width: '100%',
                height: '100%',
                fill: '#111827',
                rx: '8'
            });
            svg.appendChild(bg);
            
            // Add symbols with error handling
            try {
                planets.forEach((planet, index) => {
                    const x = 60 + index * 55;
                    const symbolGroup = utils.createSVGElement('g');
                    
                    // Circle background
                    const circle = utils.createSVGElement('circle', {
                        cx: x,
                        cy: '40',
                        r: '20',
                        fill: planet.color,
                        'fill-opacity': '0.2'
                    });
                    symbolGroup.appendChild(circle);
                    
                    // Symbol
                    const symbol = utils.createSVGElement('text', {
                        x: x,
                        y: '47',
                        'text-anchor': 'middle',
                        'font-size': '24',
                        fill: planet.color
                    });
                    symbol.textContent = planet.symbol;
                    symbolGroup.appendChild(symbol);
                    
                    // Name
                    const name = utils.createSVGElement('text', {
                        x: x,
                        y: '80',
                        'text-anchor': 'middle',
                        'font-size': '12',
                        fill: '#D1D5DB'
                    });
                    name.textContent = planet.name;
                    symbolGroup.appendChild(name);
                    
                    svg.appendChild(symbolGroup);
                });
            } catch (error) {
                console.error('Error drawing planet symbols:', error);
            }
        },
        
        // Draw zodiac wheel
        drawZodiacWheel() {
            const svg = document.getElementById('zodiac-wheel');
            if (!svg) return;
            
            const signs = [
                { name: 'Aries', symbol: '♈', color: '#EF4444' },
                { name: 'Taurus', symbol: '♉', color: '#10B981' },
                { name: 'Gemini', symbol: '♊', color: '#F59E0B' },
                { name: 'Cancer', symbol: '♋', color: '#3B82F6' },
                { name: 'Leo', symbol: '♌', color: '#F59E0B' },
                { name: 'Virgo', symbol: '♍', color: '#10B981' },
                { name: 'Libra', symbol: '♎', color: '#6366F1' },
                { name: 'Scorpio', symbol: '♏', color: '#8B5CF6' },
                { name: 'Sagittarius', symbol: '♐', color: '#EF4444' },
                { name: 'Capricorn', symbol: '♑', color: '#6B7280' },
                { name: 'Aquarius', symbol: '♒', color: '#14B8A6' },
                { name: 'Pisces', symbol: '♓', color: '#3B82F6' }
            ];
            
            svg.innerHTML = '';
            
            try {
                // Add background
                const bg = utils.createSVGElement('rect', {
                    width: '100%',
                    height: '100%',
                    fill: '#111827',
                    rx: '8'
                });
                svg.appendChild(bg);
                
                const centerX = 250;
                const centerY = 250;
                const outerRadius = 180;
                const innerRadius = 120;
                
                // Draw outer circle
                const outerCircle = utils.createSVGElement('circle', {
                    cx: centerX,
                    cy: centerY,
                    r: outerRadius,
                    fill: 'none',
                    stroke: '#4B5563',
                    'stroke-width': '1'
                });
                svg.appendChild(outerCircle);
                
                // Draw inner circle
                const innerCircle = utils.createSVGElement('circle', {
                    cx: centerX,
                    cy: centerY,
                    r: innerRadius,
                    fill: 'none',
                    stroke: '#4B5563',
                    'stroke-width': '1'
                });
                svg.appendChild(innerCircle);
                
                // Draw zodiac segments
                signs.forEach((sign, index) => {
                    const startAngle = index * 30 * Math.PI / 180;
                    const endAngle = (index + 1) * 30 * Math.PI / 180;
                    
                    // Draw segment
                    const path = utils.createSVGElement('path');
                    const x1 = centerX + innerRadius * Math.cos(startAngle);
                    const y1 = centerY + innerRadius * Math.sin(startAngle);
                    const x2 = centerX + outerRadius * Math.cos(startAngle);
                    const y2 = centerY + outerRadius * Math.sin(startAngle);
                    const x3 = centerX + outerRadius * Math.cos(endAngle);
                    const y3 = centerY + outerRadius * Math.sin(endAngle);
                    const x4 = centerX + innerRadius * Math.cos(endAngle);
                    const y4 = centerY + innerRadius * Math.sin(endAngle);
                    
                    path.setAttribute('d', `M ${x1} ${y1} L ${x2} ${y2} A ${outerRadius} ${outerRadius} 0 0 1 ${x3} ${y3} L ${x4} ${y4} A ${innerRadius} ${innerRadius} 0 0 0 ${x1} ${y1}`);
                    path.setAttribute('fill', sign.color);
                    path.setAttribute('fill-opacity', '0.1');
                    path.setAttribute('stroke', sign.color);
                    path.setAttribute('stroke-opacity', '0.5');
                    path.setAttribute('stroke-width', '1');
                    svg.appendChild(path);
                    
                    // Add dividing lines
                    const line = utils.createSVGElement('line', {
                        x1: x1,
                        y1: y1,
                        x2: x2,
                        y2: y2,
                        stroke: '#4B5563',
                        'stroke-width': '1'
                    });
                    svg.appendChild(line);
                    
                    // Add symbol
                    const middleAngle = (startAngle + endAngle) / 2;
                    const symbolRadius = (innerRadius + outerRadius) / 2;
                    const symbolX = centerX + symbolRadius * Math.cos(middleAngle);
                    const symbolY = centerY + symbolRadius * Math.sin(middleAngle);
                    
                    const symbol = utils.createSVGElement('text', {
                        x: symbolX,
                        y: symbolY,
                        'text-anchor': 'middle',
                        'dominant-baseline': 'middle',
                        'font-size': '18',
                        fill: sign.color
                    });
                    symbol.textContent = sign.symbol;
                    svg.appendChild(symbol);
                });
                
                // Add center decoration
                const centerCircle = utils.createSVGElement('circle', {
                    cx: centerX,
                    cy: centerY,
                    r: '10',
                    fill: '#6366F1',
                    'fill-opacity': '0.3',
                    stroke: '#6366F1',
                    'stroke-width': '1'
                });
                svg.appendChild(centerCircle);
            } catch (error) {
                console.error('Error drawing zodiac wheel:', error);
            }
        },
        
        // Draw houses chart
        drawHousesChart() {
            const svg = document.getElementById('houses-chart');
            if (!svg) return;
            
            svg.innerHTML = '';
            
            try {
                // Add background
                const bg = utils.createSVGElement('rect', {
                    width: '100%',
                    height: '100%',
                    fill: '#111827',
                    rx: '8'
                });
                svg.appendChild(bg);
                
                const centerX = 250;
                const centerY = 250;
                const radius = 180;
                
                // Draw outer circle
                const outerCircle = utils.createSVGElement('circle', {
                    cx: centerX,
                    cy: centerY,
                    r: radius,
                    fill: 'none',
                    stroke: '#4B5563',
                    'stroke-width': '1'
                });
                svg.appendChild(outerCircle);
                
                // Draw house lines
                for (let i = 0; i < 12; i++) {
                    const angle = i * 30 * Math.PI / 180;
                    const x2 = centerX + radius * Math.cos(angle);
                    const y2 = centerY + radius * Math.sin(angle);
                    
                    const line = utils.createSVGElement('line', {
                        x1: centerX,
                        y1: centerY,
                        x2: x2,
                        y2: y2,
                        stroke: '#4B5563',
                        'stroke-width': '1'
                    });
                    svg.appendChild(line);
                    
                    // Add house number
                    const labelRadius = radius * 0.85;
                    const labelX = centerX + labelRadius * Math.cos(angle + Math.PI/60);
                    const labelY = centerY + labelRadius * Math.sin(angle + Math.PI/60);
                    
                    const houseNumber = utils.createSVGElement('text', {
                        x: labelX,
                        y: labelY,
                        'text-anchor': 'middle',
                        'dominant-baseline': 'middle',
                        'font-size': '14',
                        fill: '#D1D5DB'
                    });
                    houseNumber.textContent = i + 1;
                    svg.appendChild(houseNumber);
                }
                
                // Add key house points
                const housePoints = [
                    { name: 'ASC', angle: 0, color: '#6366F1' },
                    { name: 'IC', angle: 90, color: '#3B82F6' },
                    { name: 'DSC', angle: 180, color: '#6366F1' },
                    { name: 'MC', angle: 270, color: '#3B82F6' }
                ];
                
                housePoints.forEach(point => {
                    const angle = point.angle * Math.PI / 180;
                    const x = centerX + radius * Math.cos(angle);
                    const y = centerY + radius * Math.sin(angle);
                    
                    // Add circle marker
                    const marker = utils.createSVGElement('circle', {
                        cx: x,
                        cy: y,
                        r: '6',
                        fill: point.color
                    });
                    svg.appendChild(marker);
                    
                    // Add label
                    const labelX = centerX + (radius + 20) * Math.cos(angle);
                    const labelY = centerY + (radius + 20) * Math.sin(angle);
                    
                    const label = utils.createSVGElement('text', {
                        x: labelX,
                        y: labelY,
                        'text-anchor': 'middle',
                        'dominant-baseline': 'middle',
                        'font-size': '14',
                        'font-weight': 'bold',
                        fill: point.color
                    });
                    label.textContent = point.name;
                    svg.appendChild(label);
                });
                
                // Add center decoration
                const centerCircle = utils.createSVGElement('circle', {
                    cx: centerX,
                    cy: centerY,
                    r: '5',
                    fill: '#6366F1'
                });
                svg.appendChild(centerCircle);
            } catch (error) {
                console.error('Error drawing houses chart:', error);
            }
        },
        
        // Draw aspect chart
        drawAspectChart() {
            const svg = document.getElementById('aspect-chart');
            if (!svg) return;
            
            svg.innerHTML = '';
            
            try {
                // Add background
                const bg = utils.createSVGElement('rect', {
                    width: '100%',
                    height: '100%',
                    fill: '#111827',
                    rx: '8'
                });
                svg.appendChild(bg);
                
                const aspects = [
                    { name: 'Conjunction', symbol: '☌', angle: '0°', color: '#FFFFFF', line: 'none' },
                    { name: 'Sextile', symbol: '⚹', angle: '60°', color: '#6366F1', line: 'dotted' },
                    { name: 'Square', symbol: '□', angle: '90°', color: '#EF4444', line: 'solid' },
                    { name: 'Trine', symbol: '△', angle: '120°', color: '#3B82F6', line: 'dotted' },
                    { name: 'Opposition', symbol: '☍', angle: '180°', color: '#F59E0B', line: 'solid' }
                ];
                
                // Draw aspect lines diagram
                const centerX = 250;
                const centerY = 100;
                const radius = 70;
                
                // Draw center circle
                const circle = utils.createSVGElement('circle', {
                    cx: centerX,
                    cy: centerY,
                    r: radius,
                    fill: 'none',
                    stroke: '#4B5563',
                    'stroke-width': '1'
                });
                svg.appendChild(circle);
                
                // Draw aspect lines
                for (let i = 0; i < 12; i++) {
                    const angle = i * 30 * Math.PI / 180;
                    const x = centerX + radius * Math.cos(angle);
                    const y = centerY + radius * Math.sin(angle);
                    
                    const point = utils.createSVGElement('circle', {
                        cx: x,
                        cy: y,
                        r: '3',
                        fill: '#6B7280'
                    });
                    svg.appendChild(point);
                }
                
                // Draw example aspect lines
                const aspectLines = [
                    { from: 0, to: 6, type: 'Opposition' },
                    { from: 0, to: 4, type: 'Trine' },
                    { from: 0, to: 3, type: 'Square' },
                    { from: 0, to: 2, type: 'Sextile' }
                ];
                
                aspectLines.forEach(line => {
                    const fromAngle = line.from * 30 * Math.PI / 180;
                    const toAngle = line.to * 30 * Math.PI / 180;
                    
                    const x1 = centerX + radius * Math.cos(fromAngle);
                    const y1 = centerY + radius * Math.sin(fromAngle);
                    const x2 = centerX + radius * Math.cos(toAngle);
                    const y2 = centerY + radius * Math.sin(toAngle);
                    
                    const aspectType = aspects.find(a => a.name === line.type);
                    
                    const aspectLine = utils.createSVGElement('line', {
                        x1: x1,
                        y1: y1,
                        x2: x2,
                        y2: y2,
                        stroke: aspectType.color,
                        'stroke-width': '2'
                    });
                    
                    if (aspectType.line === 'dotted') {
                        aspectLine.setAttribute('stroke-dasharray', '4,2');
                    }
                    
                    svg.appendChild(aspectLine);
                });
                
                // Draw aspect symbols and descriptions
                aspects.forEach((aspect, index) => {
                    const y = 200 + index * 30;
                    
                    // Symbol
                    const symbol = utils.createSVGElement('text', {
                        x: '80',
                        y: y,
                        'text-anchor': 'middle',
                        'font-size': '24',
                        fill: aspect.color
                    });
                    symbol.textContent = aspect.symbol;
                    svg.appendChild(symbol);
                    
                    // Name
                    const name = utils.createSVGElement('text', {
                        x: '150',
                        y: y,
                        'font-size': '16',
                        fill: '#D1D5DB'
                    });
                    name.textContent = aspect.name;
                    svg.appendChild(name);
                    
                    // Angle
                    const angle = utils.createSVGElement('text', {
                        x: '280',
                        y: y,
                        'font-size': '16',
                        fill: '#9CA3AF'
                    });
                    angle.textContent = aspect.angle;
                    svg.appendChild(angle);
                    
                    // Line example
                    if (aspect.line !== 'none') {
                        const line = utils.createSVGElement('line', {
                            x1: '320',
                            y1: y - 5,
                            x2: '380',
                            y2: y - 5,
                            stroke: aspect.color,
                            'stroke-width': '2'
                        });
                        
                        if (aspect.line === 'dotted') {
                            line.setAttribute('stroke-dasharray', '4,2');
                        }
                        
                        svg.appendChild(line);
                    }
                });
            } catch (error) {
                console.error('Error drawing aspect chart:', error);
            }
        }
    };
    
    // Interaction Module
    const Interactions = {
        // Initialize card interactions
        initCardInteractions() {
            const cards = document.querySelectorAll('.card-animate');
            
            cards.forEach((card, index) => {
                // Add staggered animation delay
                card.style.animationDelay = `${index * 0.1}s`;
                
                // Enhanced hover effects
                card.addEventListener('mouseenter', function() {
                    this.classList.add('shadow-lg');
                }, { passive: true });
                
                card.addEventListener('mouseleave', function() {
                    this.classList.remove('shadow-lg');
                }, { passive: true });
                
                // Keyboard navigation support
                card.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        this.click();
                    }
                });
            });
        },
        
        // Initialize lazy loading for images
        initLazyLoading() {
            const images = document.querySelectorAll('img.lazy-load');
            
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries, observer) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.classList.add('loaded');
                            observer.unobserve(img);
                        }
                    });
                }, {
                    rootMargin: '50px'
                });
                
                images.forEach(img => imageObserver.observe(img));
            } else {
                // Fallback for browsers without IntersectionObserver
                images.forEach(img => img.classList.add('loaded'));
            }
        },
        
        // Initialize smooth scroll for anchor links
        initSmoothScroll() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    const href = this.getAttribute('href');
                    if (href === '#' || href === '#!') return;
                    
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        const headerOffset = 80;
                        const elementPosition = target.getBoundingClientRect().top;
                        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                        
                        window.scrollTo({
                            top: offsetPosition,
                            behavior: 'smooth'
                        });
                    }
                });
            });
        }
    };
    
    // Performance Module
    const Performance = {
        // Preload critical resources
        preloadResources() {
            const criticalImages = [
                'https://image.ixingpan.com/uploads/wp/image/2019/07/image23.png'
            ];
            
            criticalImages.forEach(src => {
                const link = document.createElement('link');
                link.rel = 'preload';
                link.as = 'image';
                link.href = src;
                document.head.appendChild(link);
            });
        },
        
        // Optimize scroll performance
        optimizeScroll() {
            let ticking = false;
            
            const updateOnScroll = () => {
                // Scroll-based operations here
                ticking = false;
            };
            
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(updateOnScroll);
                    ticking = true;
                }
            }, { passive: true });
        }
    };
    
    // Main initialization
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', initialize);
        } else {
            initialize();
        }
    }
    
    function initialize() {
        try {
            // Draw SVG charts
            SVGChart.drawPlanetSymbols();
            SVGChart.drawZodiacWheel();
            SVGChart.drawHousesChart();
            SVGChart.drawAspectChart();
            
            // Initialize interactions
            Interactions.initCardInteractions();
            Interactions.initLazyLoading();
            Interactions.initSmoothScroll();
            
            // Performance optimizations
            Performance.preloadResources();
            Performance.optimizeScroll();
            
            // Log success
            if (process.env.NODE_ENV === 'development') {
                console.log('Astrological Guide initialized successfully');
            }
        } catch (error) {
            console.error('Error initializing Astrological Guide:', error);
        }
    }
    
    // Start initialization
    init();
    
    // Export for potential external use
    window.AstrologicalGuide = {
        SVGChart,
        Interactions,
        utils
    };
})();
