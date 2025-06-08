import { Logo } from "@/once-ui/components";

const person = {
  firstName: "Joshua",
  lastName: "Yoon",
  get name() {
    return `${this.firstName} ${this.lastName}`;
  },
  role: "Full Stack Engineer",
  avatar: "/images/avatar.jpg",
  email: "contact@joshtech.com",
  location: "Asia/Seoul", // Expecting the IANA time zone identifier, e.g., 'Europe/Vienna'
  languages: ["Korean", "English", "Japanese"], // optional: Leave the array empty if you don't want to display languages
};

const newsletter = {
  display: true,
  title: <>Subscribe to {person.firstName}&apos;s Newsletter</>,
  description: (
    <>
      I occasionally write about design, technology, and share thoughts on the intersection of
      creativity and engineering.
    </>
  ),
};

const social = [
  // Links are automatically displayed.
  // Import new icons in /once-ui/icons.ts
  {
    name: "GitHub",
    icon: "github",
    link: "https://github.com/joshua92y/",
  },
  {
    name: "LinkedIn",
    icon: "linkedin",
    link: "https://www.linkedin.com/in/joshua-yoon-1bb7a4365/",
  },
  {
    name: "X",
    icon: "x",
    link: "",
  },
  {
    name: "Email",
    icon: "email",
    link: `mailto:${person.email}`,
  },
];

const home = {
  path: "/",
  image: "/images/og/home.jpg",
  label: "Home",
  title: `${person.name}'s Portfolio`,
  description: `Portfolio website showcasing my work as a ${person.role}`,
  headline: <>Crafting the unseen. Delivering the seen. Bridging systems and stories.</>,
  featured: {
    display: true,
    title: (
      <>
        Recent project: <strong className="ml-4">AI-Powered Market Analysis & Chatbot</strong>
      </>
    ),
    href: "/work/building-an-ai-powered-market-analysis-chatbot-system",
  },
  subline: (
    <>
      I&apos;m joshua, a Full stack engineer at{" "}
      <Logo icon={false} style={{ display: "inline-flex", top: "0.25em", marginLeft: "-0.25em" }} />
      , where I craft intuitive
      <br /> user experiences. After hours, I build my own projects. I enjoy studying in unfamiliar
      places to gain new inspiration.
      <br />
      <a href="https://joshuatech.dev/blog" target="_blank" rel="noopener noreferrer">
        - View my development notes and learnings
      </a>
      .
    </>
  ),
};

const about = {
  path: "/about",
  label: "About",
  title: `About – ${person.name}`,
  description: `Meet ${person.name}, ${person.role} from ${person.location}`,
  tableOfContent: {
    display: true,
    subItems: false,
  },
  avatar: {
    display: true,
  },
  calendar: {
    display: true,
    link: "https://cal.com",
  },
  intro: {
    display: true,
    title: "Introduction",
    description: (
      <>
        I shape ideas into experiences, and connect possibilities to reality.
        <br />
        Hi, I&apos;m Joshua, a Full Stack Engineer at joshuatech, dedicated to building digital
        solutions that resonate deeply with users. Beyond professional boundaries, I&apos;m always
        experimenting with side projects, driven by curiosity and fueled by inspiration gathered
        from new environments and experiences.
      </>
    ),
  },
  work: {
    display: true, // set to false to hide this section
    title: "Work Experience",
    experiences: [
      {
        company: "joshuatech",
        timeframe: "2024 - Present",
        role: "Full Stack Engineer",
        achievements: [
          <>
            Building main backend services (Django), microservice backends (FastAPI), and caching
            servers (Dragonfly) on Oracle servers, and developing a frontend using Next.js 15 on
            Cloudflare. Utilizing Neon DB and Qdrant vector DB to create and manage databases.
          </>,
          <>This is joshuatech&apos;s main project to connect all platform services.</>,
        ],
        images: [
          // optional: leave the array empty if you don't want to display images
          {
            src: "/images/projects/project-01/cover-01.jpg",
            alt: "Once UI Project",
            width: 16,
            height: 9,
          },
        ],
      },
      {
        company: "joshuatech",
        timeframe: "2024 - Present",
        role: "Full Stack Engineer",
        achievements: [
          <>
            Developing &quot;Tone Change&quot; application as a Full Stack Engineer using FastAPI on
            Railway for backend and Flutter frontend deployed via GitHub. It analyzes and converts
            users&apos; speech styles using AI.
          </>,
        ],
        images: [],
      },
    ],
  },
  studies: {
    display: true, // set to false to hide this section
    title: "Studies",
    institutions: [
      {
        name: "AIX",
        description: <>Completed a 6-month full stack engineering course.</>,
      },
      {
        name: "Jangan University",
        description: <>Majored in Distribution Management.</>,
      },
    ],
  },
  technical: {
    display: true, // set to false to hide this section
    title: "Technical skills",
    skills: [
      {
        title: "TensorFlow, PyTorch",
        description: (
          <>Quickly learns and extracts meaningful data using machine learning modules.</>
        ),
        // optional: leave the array empty if you don't want to display images
        images: [
          {
            src: "/images/projects/project-01/cover-02.jpg",
            alt: "Project image",
            width: 16,
            height: 9,
          },
          {
            src: "/images/projects/project-01/cover-03.jpg",
            alt: "Project image",
            width: 16,
            height: 9,
          },
        ],
      },
      {
        title: "Django, FastAPI",
        description: (
          <>
            Efficiently creates optimized work using Python frameworks suitable for each scenario.
          </>
        ),
        // optional: leave the array empty if you don't want to display images
        images: [
          {
            src: "/images/projects/project-01/cover-04.jpg",
            alt: "Project image",
            width: 16,
            height: 9,
          },
        ],
      },
      {
        title: "Next.js, Flutter",
        description: (
          <>
            Emphasizes SEO and user experience, leveraging marketing experience to increase
            discoverability. Rapidly builds multi-platform MVPs using Flutter.
          </>
        ),
        // optional: leave the array empty if you don't want to display images
        images: [
          {
            src: "/images/projects/project-01/cover-04.jpg",
            alt: "Project image",
            width: 16,
            height: 9,
          },
        ],
      },
    ],
  },
};

const blog = {
  path: "/blog",
  label: "Blog",
  title: "Joshua’s Digital Playground",
  description: `Read what ${person.name} has been up to recently`,
  // Create new blog posts by adding a new .mdx file to app/blog/posts
  // All posts will be listed on the /blog route
};

const work = {
  path: "/work",
  label: "Work",
  title: `Projects – ${person.name}`,
  description: `Design and dev projects by ${person.name}`,
  // Create new project pages by adding a new .mdx file to app/blog/posts
  // All projects will be listed on the /home and /work routes
};

const gallery = {
  path: "/gallery",
  label: "Gallery",
  title: `Photo gallery – ${person.name}`,
  description: `A photo collection by ${person.name}`,
  // Images by https://lorant.one
  // These are placeholder images, replace with your own
  images: [
    {
      src: "/images/gallery/avarice.jpg",
      alt: "avarice",
      orientation: "vertical",
    },
    {
      src: "/images/gallery/HanRiver_Twilight.jpg",
      alt: "HanRiver_Twilight",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/Jeongdongjin_sunrise.jpg",
      alt: "Jeongdongjin_sunrise",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/futsal.jpg",
      alt: "futsal",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/lunar_eclipse.jpg",
      alt: "lunar_eclipse",
      orientation: "square",
    },
    {
      src: "/images/gallery/campfire.jpg",
      alt: "campfire",
      orientation: "vertical",
    },
    {
      src: "/images/gallery/neon_crew.jpg",
      alt: "neon_crew",
      orientation: "horizontal",
    },
    {
      src: "/images/gallery/avatar_1.jpg",
      alt: "avatar_1",
      orientation: "vertical",
    },
  ],
};

export { person, social, newsletter, home, about, blog, work, gallery };
